# 📝 快速本地部署指南（5分钟上手）

## 🎯 你需要做的（3步）

### 第1步：准备环境（2分钟）

1. **安装 Python**（如果还没有）
   - 下载：https://www.python.org/downloads/
   - ⚠️ 安装时勾选 "Add Python to PATH"
   - 验证：打开命令行，输入 `python --version`

2. **安装依赖**（在命令行运行）
   ```batch
   pip install fastapi uvicorn langchain langchain-openai langgraph openai aiohttp websockets coze-coding-dev-sdk
   ```

---

### 第2步：创建项目文件夹（1分钟）

```batch
# 在桌面创建项目文件夹
mkdir historical-chat
cd historical-chat

# 创建子文件夹
mkdir src\agents
mkdir src\tools
mkdir src\api\routes
mkdir src\storage\memory
mkdir config
mkdir assets
mkdir frontend
```

---

### 第3步：复制文件并启动（2分钟）

#### A. 复制以下文件到对应文件夹

**从当前环境复制这些文件**：

| 源文件 | 目标位置 |
|--------|----------|
| config/agent_llm_config.json | config/agent_llm_config.json |
| assets/historical_figures.json | assets/historical_figures.json |
| src/app.py | src/app.py |
| src/agents/agent.py | src/agents/agent.py |
| src/tools/historical_figure_tool.py | src/tools/historical_figure_tool.py |
| src/api/__init__.py | src/api/__init__.py |
| src/api/routes/chat.py | src/api/routes/chat.py |
| src/api/routes/websocket.py | src/api/routes/websocket.py |
| src/api/routes/voice.py | src/api/routes/voice.py |
| src/api/routes/model3d.py | src/api/routes/model3d.py |
| src/storage/memory/memory_saver.py | src/storage/memory/memory_saver.py |
| frontend/index.html | frontend/index.html |
| requirements.txt | requirements.txt |

**复制方式**：
- 方式1：使用文本编辑器打开每个文件，复制内容，粘贴到本地创建的同名文件中
- 方式2：如果可以下载，直接下载整个项目文件夹

#### B. 启动服务

**启动后端**（打开命令行窗口）：
```batch
cd C:\Users\你的用户名\Desktop\historical-chat
set PYTHONPATH=%PYTHONPATH%;%CD%\src
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

**启动前端**（再打开一个命令行窗口）：
```batch
cd C:\Users\你的用户名\Desktop\historical-chat\frontend
python -m http.server 3000
```

#### C. 访问应用

打开浏览器，访问：
```
http://localhost:3000
```

---

## ✅ 完成！

现在你可以在本地与历史人物对话了！

**预设人物**：
- 🏮 李白
- 📜 孔子
- 🔬 爱因斯坦
- 🎭 莎士比亚
- 💭 苏格拉底
- 🌊 屈原
- 🔍 牛顿
- 🎨 达芬奇

---

## ❓ 遇到问题？

### 问题1：pip install 失败

**解决**：使用国内镜像
```batch
pip install fastapi uvicorn langchain langchain-openai langgraph openai aiohttp websockets coze-coding-dev-sdk -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题2：找不到 uvicorn 命令

**解决**：使用 python -m 方式
```batch
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000
```

### 问题3：端口被占用

**解决**：修改端口号
```batch
uvicorn src.app:app --host 0.0.0.0 --port 8888
```
然后修改 frontend/index.html 中的：
```javascript
const API_BASE = 'http://localhost:8888';
```

### 问题4：启动后报错

**解决**：检查
1. Python 版本是否 >= 3.9
2. 所有依赖是否安装成功
3. 文件结构是否正确
4. PYTHONPATH 是否设置正确

---

## 📚 详细文档

- [完整本地部署指南](./LOCAL_SETUP.md) - 详细的部署步骤和故障排查
- [文件清单](./EXPORT_MANIFEST.txt) - 所有需要复制的文件列表

---

## 💡 提示

1. **创建虚拟环境**（推荐）：
   ```batch
   python -m venv venv
   venv\Scripts\activate
   ```

2. **检查文件结构**：
   ```
   historical-chat/
   ├── config/
   │   └── agent_llm_config.json
   ├── assets/
   │   └── historical_figures.json
   ├── src/
   │   ├── agents/
   │   │   └── agent.py
   │   ├── tools/
   │   │   └── historical_figure_tool.py
   │   ├── api/
   │   │   ├── __init__.py
   │   │   └── routes/
   │   │       ├── chat.py
   │   │       ├── websocket.py
   │   │       ├── voice.py
   │   │       └── model3d.py
   │   ├── storage/
   │   │   └── memory/
   │   │       └── memory_saver.py
   │   └── app.py
   ├── frontend/
   │   └── index.html
   └── requirements.txt
   ```

3. **关闭服务**：在对应的命令行窗口按 `Ctrl+C`

---

祝你使用愉快！🎉
