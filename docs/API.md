# 历史人物对话 API 文档

## 概述

这是历史人物对话系统的后端 API，提供 RESTful API 和 WebSocket 实时对话接口。

## 启动服务器

```bash
# 方法 1: 使用启动脚本
./scripts/start_api.sh

# 方法 2: 直接运行
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

服务器启动后，可以访问：
- API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## API 接口

### 1. 获取历史人物列表

**接口**: `GET /api/figures/`

**响应示例**:
```json
{
  "figures": [
    {
      "name": "李白",
      "title": "诗仙",
      "era": "唐代（701年－762年）",
      "style": "豪放飘逸、洒脱不羁、充满想象力、文采飞扬",
      "famous_works": ["将进酒", "静夜思", ...]
    },
    ...
  ],
  "count": 8,
  "default": "李白"
}
```

### 2. 获取历史人物详情

**接口**: `GET /api/figures/detail/{figure_name}`

**参数**:
- `figure_name`: 历史人物名称

**响应示例**:
```json
{
  "name": "李白",
  "title": "诗仙",
  "era": "唐代（701年－762年）",
  "style": "豪放飘逸、洒脱不羁、充满想象力、文采飞扬",
  "famous_works": ["将进酒", "静夜思", ...],
  "system_prompt": "你是李白，唐代伟大的浪漫主义诗人..."
}
```

### 3. 发送消息（REST API）

**接口**: `POST /api/chat/`

**请求体**:
```json
{
  "message": "你好，你是谁？",
  "figure_name": "李白",
  "session_id": "optional-session-id",
  "stream": false
}
```

**响应示例**:
```json
{
  "message": "哈哈，足下何人？某虽浪迹天涯...",
  "figure_name": "李白",
  "session_id": "generated-or-provided-session-id"
}
```

### 4. 获取对话历史

**接口**: `GET /api/chat/history/{session_id}`

**参数**:
- `session_id`: 会话ID

**响应示例**:
```json
{
  "session_id": "test-session-001",
  "history": [
    {"role": "user", "content": "请扮演李白与我对话。你好"},
    {"role": "assistant", "content": "哈哈，足下何人？..."}
  ],
  "count": 2
}
```

### 5. 清除对话历史

**接口**: `DELETE /api/chat/history/{session_id}`

**参数**:
- `session_id`: 会话ID

## WebSocket 接口

### 连接

**地址**: `ws://localhost:8000/api/ws/chat`

**参数**:
- `session_id`: 可选，会话ID。如果不提供，将自动生成

### 消息格式

**客户端发送**:
```json
{
  "type": "message",
  "content": "用户消息",
  "figure_name": "可选，历史人物名称"
}
```

**服务器响应（连接成功）**:
```json
{
  "type": "connected",
  "session_id": "auto-generated-id",
  "message": "WebSocket 连接成功"
}
```

**服务器响应（流式输出）**:
```json
{
  "type": "chunk",
  "content": "流式输出内容片段",
  "figure_name": "历史人物名称",
  "session_id": "会话ID"
}
```

**服务器响应（完成）**:
```json
{
  "type": "done",
  "session_id": "会话ID"
}
```

**服务器响应（错误）**:
```json
{
  "type": "error",
  "message": "错误描述"
}
```

## 测试脚本

### 测试 REST API

```bash
python scripts/test_api.py
```

### 测试 WebSocket

```bash
python scripts/test_websocket.py
```

## 使用示例

### Python 客户端示例

```python
import requests

# 获取人物列表
response = requests.get("http://localhost:8000/api/figures/")
figures = response.json()

# 发送消息
data = {
    "message": "你好，我是谁？",
    "figure_name": "李白"
}
response = requests.post("http://localhost:8000/api/chat/", json=data)
result = response.json()
print(result["message"])
```

### WebSocket 客户端示例

```python
import asyncio
import websockets
import json

async def chat():
    uri = "ws://localhost:8000/api/ws/chat"

    async with websockets.connect(uri) as websocket:
        # 接收连接确认
        welcome = await websocket.recv()
        print(json.loads(welcome))

        # 发送消息
        message = {
            "type": "message",
            "content": "你好，你是谁？",
            "figure_name": "李白"
        }
        await websocket.send(json.dumps(message))

        # 接收流式响应
        while True:
            response = await websocket.recv()
            data = json.loads(response)

            if data["type"] == "chunk":
                print(data["content"], end="", flush=True)
            elif data["type"] == "done":
                print("\n对话完成")
                break

asyncio.run(chat())
```

## 注意事项

1. **会话管理**: 使用 `session_id` 来维护对话上下文。相同的 `session_id` 会保持对话历史。

2. **人物选择**: 可以通过消息内容指定人物（如 "请扮演李白与我对话"）或通过 `figure_name` 参数指定。

3. **动态人物**: 支持与未预设的历史人物对话，系统会自动搜索并创建人物角色。

4. **流式输出**: WebSocket 接口提供打字机效果的流式输出，延迟设置为 0.02 秒/字符。

5. **CORS**: 默认允许所有来源，生产环境应该配置具体的允许域名。

## 错误处理

所有接口返回标准的 HTTP 状态码：
- `200 OK`: 请求成功
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器错误

错误响应格式：
```json
{
  "detail": "错误描述"
}
```
