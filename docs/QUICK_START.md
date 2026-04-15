# 🚀 本地部署快速参考

## 一分钟快速开始

### Windows 用户

```batch
# 1. 运行检查脚本
scripts\check_deployment.bat

# 2. 启动后端（终端1）
python -m uvicorn src.app:app --port 8000

# 3. 启动前端（终端2）
cd frontend
python -m http.server 3000

# 4. 打开浏览器
访问: http://localhost:3000
```

### macOS/Linux 用户

```bash
# 1. 运行检查脚本
bash scripts/check_deployment.sh

# 2. 启动后端（终端1）
python -m uvicorn src.app:app --port 8000

# 3. 启动前端（终端2）
cd frontend
python -m http.server 3000

# 4. 打开浏览器
访问: http://localhost:3000
```

---

## 📦 项目文件

项目文件已打包：`/workspace/projects_backup.tar.gz`（177MB）

**下载后解压**：
```bash
tar -xzf projects_backup.tar.gz
cd projects
```

---

## ⚙️ 环境要求

- Python 3.9 或更高版本
- 端口 8000 和 3000 未被占用
- 现代浏览器（Chrome/Edge/Firefox/Safari 14+）

---

## 🔧 安装依赖

**使用 uv（推荐，速度快）**：
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync
```

**使用 pip**：
```bash
pip install -r requirements.txt
```

---

## 🚀 启动方式

### 方式 1：使用检查脚本（推荐）

**Windows**：
```batch
scripts\check_deployment.bat
```

**macOS/Linux**：
```bash
bash scripts/check_deployment.sh
```

### 方式 2：使用快速启动脚本

**macOS/Linux**：
```bash
bash scripts/quick_start.sh
# 然后在新终端启动前端
cd frontend
python -m http.server 3000
```

### 方式 3：手动启动

**终端 1 - 后端**：
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m uvicorn src.app:app --port 8000
```

**终端 2 - 前端**：
```bash
cd frontend
python -m http.server 3000
```

---

## 🌐 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端界面 | http://localhost:3000 | 主界面 |
| 后端 API | http://localhost:8000 | API 服务 |
| API 文档 | http://localhost:8000/docs | Swagger 文档 |

---

## 🧪 测试

```bash
# 测试后端健康检查
curl http://localhost:8000/health

# 运行 API 测试
python scripts/test_api.py

# 运行语音测试
python scripts/test_voice.py
```

---

## ❓ 常见问题速查

| 问题 | 解决方案 |
|------|----------|
| 端口被占用 | 换端口：`--port 8080` |
| 依赖安装失败 | 使用 uv 代替 pip |
| 前端无法连接后端 | 检查后端是否运行 |
| 3D 模型不显示 | 检查浏览器 WebGL 支持 |
| 语音播放失败 | 检查音频 URL 是否过期 |

---

## 📚 详细文档

- [完整本地部署指南](./LOCAL_DEPLOYMENT.md)
- [API 文档](./API.md)
- [语音 API 文档](./VOICE_API.md)
- [3D API 文档](./3D_API.md)
- [前端使用文档](../frontend/README.md)

---

## ✅ 检查清单

- [ ] Python 3.9+ 已安装
- [ ] 所有依赖已安装
- [ ] 端口 8000 和 3000 可用
- [ ] 后端服务已启动
- [ ] 前端服务已启动
- [ ] 可以访问 http://localhost:3000
- [ ] 可以选择历史人物
- [ ] 可以发送消息并收到回复

---

## 🎯 使用流程

1. **打开浏览器** → http://localhost:3000
2. **选择人物** → 点击"切换人物"
3. **输入消息** → 在右侧输入框
4. **发送** → 点击"发送"按钮
5. **体验** → AI 以历史人物身份回复
6. **播放语音** → 点击"播放语音"按钮
7. **查看 3D 模型** → 左侧展示区

---

## 🛑 停止服务

**终端中按 `Ctrl+C`** 或关闭终端

---

**祝使用愉快！🎉**

如有问题，请查看详细文档：[LOCAL_DEPLOYMENT.md](./LOCAL_DEPLOYMENT.md)
