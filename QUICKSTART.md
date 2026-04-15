# 🚀 快速开始（重要必读）

## ⚠️ Windows 用户注意

**不要双击 `.bat` 文件！**

❌ 错误方式：双击 `scripts\check_deployment.bat`  
✅ 正确方式：在命令提示符中运行

### Windows 用户正确运行方式：

**步骤**：
1. 按 `Win + R`，输入 `cmd`，按 Enter
2. 导航到项目目录：
   ```batch
   cd C:\你的项目路径\projects
   ```
3. 运行脚本：
   ```batch
   scripts\check_deployment_safe.bat
   ```

详细说明请查看：[Windows 脚本运行指南](./docs/WINDOWS_SCRIPT_GUIDE.md)

---

## 📦 快速部署（所有平台）

### 1. 环境要求
- Python 3.9 或更高版本
- 端口 8000 和 3000 未被占用

### 2. 安装依赖
```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 3. 启动服务

**终端 1 - 启动后端**：
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m uvicorn src.app:app --port 8000
```

**终端 2 - 启动前端**：
```bash
cd frontend
python -m http.server 3000
```

### 4. 访问应用
- 前端：http://localhost:3000
- 后端：http://localhost:8000
- API 文档：http://localhost:8000/docs

---

## 📚 详细文档

- [Windows 脚本运行指南](./docs/WINDOWS_SCRIPT_GUIDE.md) - **Windows 用户必读**
- [快速参考](./docs/QUICK_START.md) - 一分钟快速开始
- [本地部署完整指南](./docs/LOCAL_DEPLOYMENT.md) - 详细步骤
- [API 文档](./docs/API.md) - 后端接口
- [前端文档](./frontend/README.md) - 前端使用

---

# 历史人物沉浸式对话系统

## 📖 项目简介

这是一个基于 AI 的沉浸式历史人物对话系统，用户可以选择与不同的历史人物（如李白、孔子、爱因斯坦等）进行实时对话。系统支持多角色扮演、语音交互、3D 模型展示和口型同步等功能。
