# 🏠 本地部署完整指南

## 📦 部署方式对比

| 方式 | 说明 | 适合人群 |
|------|------|----------|
| **方式 A** | 下载代码到本地 | 推荐用于开发和测试 |
| **方式 B** | 使用 Docker（简化） | 推荐用于快速体验 |

---

## 🚀 方式 A：本地部署（推荐）

### 第一步：准备环境

#### 1. 安装 Python

- 下载：https://www.python.org/downloads/
- **必须**：安装时勾选 ✅ "Add Python to PATH"
- 推荐版本：Python 3.9 或 3.10

验证安装：
```batch
python --version
```

#### 2. 安装依赖包

创建项目文件夹，然后在命令行中运行：

```batch
# 创建项目目录
mkdir historical-chat
cd historical-chat

# 下载项目文件（需要从当前环境复制）
# 见下方"获取项目文件"部分

# 安装依赖
pip install fastapi uvicorn
pip install langchain langchain-openai langgraph
pip install openai aiohttp websockets
pip install coze-coding-dev-sdk
```

或使用 requirements.txt：
```batch
pip install -r requirements.txt
```

#### 3. 配置环境变量

创建 `.env` 文件（在项目根目录）：

```env
COZE_WORKLOAD_IDENTITY_API_KEY=你的API密钥
COZE_INTEGRATION_MODEL_BASE_URL=https://api.coze.cn/open_api/v2
```

---

### 第二步：获取项目文件

你需要将以下文件从沙箱环境复制到本地：

**必需文件**：
```
historical-chat/
├── src/
│   ├── agents/
│   │   └── agent.py
│   ├── tools/
│   │   └── historical_figure_tool.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── websocket.py
│   │   │   ├── voice.py
│   │   │   └── model3d.py
│   │   └── __init__.py
│   ├── storage/
│   │   └── memory/
│   │       └── memory_saver.py
│   └── app.py
├── config/
│   └── agent_llm_config.json
├── assets/
│   └── historical_figures.json
├── frontend/
│   └── index.html
└── requirements.txt
```

---

### 第三步：启动服务

**启动后端**（新建一个命令行窗口）：

```batch
cd historical-chat
set PYTHONPATH=%PYTHONPATH%;%CD%\src
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

**启动前端**（新建另一个命令行窗口）：

```batch
cd historical-chat\frontend
python -m http.server 3000
```

---

### 第四步：访问应用

打开浏览器，访问：
```
http://localhost:3000
```

---

## 🐳 方式 B：Docker 部署（简化）

### 第一步：安装 Docker

- 下载：https://www.docker.com/products/docker-desktop/
- 安装并启动 Docker Desktop

### 第二步：创建 Dockerfile

创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/
COPY assets/ ./assets/
COPY frontend/ ./frontend/

ENV PYTHONPATH=/app/src

EXPOSE 8000 3000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 第三步：构建并运行

```batch
# 构建镜像
docker build -t historical-chat .

# 运行容器
docker run -d -p 8000:8000 -p 3000:3000 historical-chat
```

### 第四步：访问应用

```
http://localhost:3000
```

---

## 🔧 常见问题

### Q1: pip install 失败

**解决**：使用国内镜像
```batch
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 找不到 uvicorn 命令

**解决**：使用 python -m 方式
```batch
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000
```

### Q3: 端口被占用

**解决**：修改端口号
```batch
# 使用其他端口
uvicorn src.app:app --host 0.0.0.0 --port 8888
```

### Q4: 前端无法连接后端

**解决**：检查 frontend/index.html 中的 API_BASE 地址
```javascript
const API_BASE = 'http://localhost:8000';
```

---

## 📝 文件清单

### 后端文件
- `src/app.py` - FastAPI 主应用
- `src/agents/agent.py` - Agent 核心逻辑
- `src/tools/historical_figure_tool.py` - 历史人物工具
- `src/api/routes/chat.py` - 对话接口
- `src/api/routes/websocket.py` - WebSocket 接口
- `src/api/routes/voice.py` - 语音接口
- `src/api/routes/model3d.py` - 3D 模型接口

### 配置文件
- `config/agent_llm_config.json` - Agent 配置
- `assets/historical_figures.json` - 历史人物数据
- `requirements.txt` - Python 依赖

### 前端文件
- `frontend/index.html` - 主界面

---

## 💡 快速开始（完整命令序列）

```batch
# 1. 创建项目目录
mkdir historical-chat
cd historical-chat

# 2. 创建虚拟环境（可选但推荐）
python -m venv venv
venv\Scripts\activate

# 3. 安装依赖
pip install fastapi uvicorn langchain langchain-openai langgraph openai aiohttp websockets coze-coding-dev-sdk

# 4. 创建目录结构
mkdir src\agents
mkdir src\tools
mkdir src\api\routes
mkdir src\storage\memory
mkdir config
mkdir assets
mkdir frontend

# 5. 复制所有文件到对应目录

# 6. 启动后端
set PYTHONPATH=%PYTHONPATH%;%CD%\src
uvicorn src.app:app --host 0.0.0.0 --port 8000

# 7. 启动前端（新窗口）
cd frontend
python -m http.server 3000

# 8. 访问
# 浏览器打开 http://localhost:3000
```

---

## 📞 需要帮助？

如果遇到问题，请检查：
1. Python 版本是否 >= 3.9
2. 依赖是否全部安装成功
3. 文件结构是否正确
4. 端口是否被占用
5. API 密钥是否配置

