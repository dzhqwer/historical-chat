# 本地部署完整指南

## 📦 方式一：下载项目文件（推荐）

### 1. 下载压缩包

项目文件已打包为：`/workspace/projects_backup.tar.gz`（177MB）

**下载方式**：
- 使用 IDE 的下载功能
- 或使用命令行工具下载到本地

### 2. 在本地解压

```bash
# 在本地电脑上
tar -xzf projects_backup.tar.gz
cd projects
```

---

## 🖥️ 方式二：手动复制文件

如果压缩包太大，可以只复制必要文件：

### 必需文件清单：

**后端文件**：
```
src/
├── app.py
├── agents/
│   └── agent.py
├── api/
│   ├── app.py
│   └── routes/
│       ├── chat.py
│       ├── figures.py
│       ├── websocket.py
│       ├── voice.py
│       └── model3d.py
├── tools/
│   └── historical_figure_tool.py
└── storage/
    └── memory/
        └── memory_saver.py

config/
└── agent_llm_config.json

assets/
├── historical_figures.json
└── 3d_models.json（运行时自动生成）

pyproject.toml
uv.lock
```

**前端文件**：
```
frontend/
└── index.html
```

**脚本文件**（可选）：
```
scripts/
├── start_api.sh
└── start_all.sh
```

---

## 🛠️ 环境准备

### 1. 安装 Python

**Windows**：
- 访问：https://www.python.org/downloads/
- 下载并安装 Python 3.9 或更高版本
- 安装时勾选 "Add Python to PATH"

**macOS**：
```bash
# 使用 Homebrew
brew install python@3.9
```

**Linux**：
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.9 python3.9-venv

# CentOS/RHEL
sudo yum install python39
```

### 2. 验证 Python 安装

```bash
python --version
# 或
python3 --version
```

---

## 📥 安装依赖

### 方法 A：使用 uv（推荐，速度快）

**安装 uv**：
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**安装项目依赖**：
```bash
cd projects
uv sync
```

### 方法 B：使用 pip（传统方式）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**如果没有 requirements.txt，手动安装**：
```bash
pip install fastapi uvicorn python-multipart requests websockets coze-coding-dev-sdk
```

---

## ⚙️ 配置修改

### 1. 检查环境变量

后端需要以下环境变量：

**方式 A：创建 .env 文件**
```bash
# 在项目根目录创建 .env 文件
touch .env
```

```bash
# .env 文件内容
COZE_WORKSPACE_PATH=/path/to/projects
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
```

**方式 B：临时设置（Linux/macOS）**
```bash
export COZE_WORKSPACE_PATH=$(pwd)
export COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
export COZE_INTEGRATION_MODEL_BASE_URL=your_base_url
```

**方式 C：在代码中临时修改**

如果只是测试，可以暂时不设置环境变量，系统会使用默认值。

### 2. 检查 API 配置

查看 `config/agent_llm_config.json`：

```json
{
  "config": {
    "model": "doubao-seed-1-8-251228",
    "temperature": 0.7,
    ...
  },
  "sp": "系统提示词",
  "tools": ["select_historical_figure"]
}
```

**注意**：如果你使用的是自定义 API，需要修改模型配置。

---

## 🚀 启动服务

### 方法 A：使用启动脚本（推荐）

**启动后端**：
```bash
# macOS/Linux
bash scripts/start_api.sh

# Windows Git Bash
bash scripts/start_api.sh

# Windows PowerShell
.\scripts\start_api.ps1
```

**启动全部服务（后端 + 前端）**：
```bash
# macOS/Linux
bash scripts/start_all.sh

# Windows Git Bash
bash scripts/start_all.sh
```

### 方法 B：手动启动

**终端 1 - 启动后端**：
```bash
cd projects

# 设置环境变量（如果需要）
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 启动后端
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

**终端 2 - 启动前端**：
```bash
cd projects/frontend

# 使用 Python 启动
python -m http.server 3000

# 或使用其他工具
# npx http-server -p 3000
# php -S localhost:3000
```

---

## 🌐 访问应用

### 1. 打开浏览器

访问地址：
- **前端界面**：http://localhost:3000
- **后端 API**：http://localhost:8000
- **API 文档**：http://localhost:8000/docs

### 2. 使用功能

1. **选择历史人物**
   - 点击右上角"切换人物"
   - 选择你想对话的人物（如李白、孔子、爱因斯坦）

2. **开始对话**
   - 在右侧输入框输入消息
   - 点击"发送"或按 Enter 键
   - AI 会以该历史人物的身份回复

3. **播放语音**
   - 点击 AI 回复下方的"播放语音"按钮
   - 可以听到 AI 的语音回复

4. **查看 3D 模型**
   - 左侧会显示 3D 模型展示
   - 会有浮动动画效果
   - 说话时有缩放动画

---

## 🧪 测试服务

### 测试后端 API

```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试获取人物列表
curl http://localhost:8000/api/figures/

# 测试对话
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"你好","figure_name":"李白","session_id":"test"}'
```

### 运行测试脚本

```bash
# 测试所有 API
python scripts/test_api.py

# 测试语音功能
python scripts/test_voice.py

# 测试 3D 功能
python scripts/test_3d.py
```

---

## ❓ 常见问题

### Q1: 启动时提示 "No module named 'xxx'"

**解决**：
```bash
# 重新安装依赖
uv sync
# 或
pip install 缺失的模块名
```

### Q2: 端口被占用

**错误信息**：`Address already in use`

**解决**：
```bash
# 查找占用端口的进程
# macOS/Linux
lsof -i :8000
# Windows
netstat -ano | findstr :8000

# 终止进程
# macOS/Linux
kill -9 PID
# Windows
taskkill /PID PID /F

# 或更换端口
python -m uvicorn src.app:app --port 8080
```

### Q3: 前端无法连接后端

**检查**：
1. 后端是否启动：访问 http://localhost:8000/health
2. 前端 API 地址是否正确：检查 `frontend/index.html` 中的 `API_BASE`
3. 防火墙是否阻止：临时关闭防火墙测试

### Q4: 对话返回错误

**检查**：
1. API 密钥是否配置正确
2. 网络连接是否正常
3. 查看后端日志中的错误信息

### Q5: 语音播放失败

**检查**：
1. 音频 URL 是否过期（24 小时有效期）
2. 浏览器是否支持音频播放
3. 查看浏览器控制台的错误信息

### Q6: 3D 模型不显示

**检查**：
1. 是否生成了人物图像（调用 3D API）
2. 浏览器是否支持 WebGL
3. 查看浏览器控制台的错误信息

**测试 WebGL 支持**：
访问：https://get.webgl.org/

---

## 📝 开发调试

### 启用调试模式

```bash
# 后端启用自动重载
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### 查看日志

后端日志会显示在终端中，包含：
- API 请求信息
- 错误堆栈
- Agent 执行过程

### 修改代码后

由于使用了 `--reload` 参数，修改代码后会自动重启服务。

---

## 🔧 高级配置

### 修改默认端口

**后端端口**：
```bash
python -m uvicorn src.app:app --port 8080
```

**前端端口**：
```bash
python -m http.server 8080
```

### 修改模型配置

编辑 `config/agent_llm_config.json`：
```json
{
  "config": {
    "model": "your-model-name",
    "temperature": 0.7,
    ...
  }
}
```

### 添加新的历史人物

编辑 `assets/historical_figures.json`：
```json
{
  "figures": {
    "新人名": {
      "name": "新人名",
      "title": "称号",
      "era": "时代",
      "style": "风格描述",
      "famous_works": ["作品1", "作品2"],
      "system_prompt": "详细的角色设定"
    }
  }
}
```

---

## 🎯 性能优化

### 1. 使用生产级 ASGI 服务器

```bash
# 安装 gunicorn
pip install gunicorn uvicorn

# 启动
gunicorn src.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. 启用缓存

```bash
# 安装 Redis
pip install redis

# 在代码中添加缓存逻辑
```

### 3. 使用 Nginx 反向代理

参考 `nginx.conf` 配置文件。

---

## 📚 后续步骤

1. **测试所有功能**
   - 对话功能
   - 语音播放
   - 3D 模型展示
   - 角色切换

2. **根据需求调整**
   - 修改模型参数
   - 添加新的人物
   - 优化 UI 样式

3. **部署到生产环境**
   - 使用 Docker
   - 部署到云服务器
   - 配置 HTTPS

---

## 🆘 获取帮助

如果遇到问题：

1. 查看后端日志输出
2. 检查浏览器控制台
3. 查看本文档的"常见问题"部分
4. 查看项目中的其他文档：
   - `docs/API.md` - API 文档
   - `docs/VOICE_API.md` - 语音 API 文档
   - `docs/3D_API.md` - 3D API 文档
   - `frontend/README.md` - 前端文档

---

## ✅ 检查清单

部署前检查：
- [ ] Python 3.9+ 已安装
- [ ] uv 或 pip 已安装
- [ ] 所有依赖已安装
- [ ] 端口 8000 和 3000 未被占用
- [ ] 防火墙允许访问
- [ ] 浏览器支持 WebGL（用于 3D 展示）

启动后检查：
- [ ] 后端服务正常运行
- [ ] 前端服务正常运行
- [ ] 可以访问 http://localhost:3000
- [ ] 可以选择历史人物
- [ ] 可以发送消息
- [ ] AI 可以正常回复

---

**祝你部署成功！🎉**

如有问题，请根据"常见问题"部分排查，或查看详细文档。
