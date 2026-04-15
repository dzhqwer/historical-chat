# 🚀 快速开始

## ⚡ Windows 用户（最简单方式）

### 一键启动

```batch
# 步骤 1: 双击运行环境检查
scripts\setup_windows.bat

# 步骤 2: 双击自动启动服务
scripts\auto_start.bat
```

然后在浏览器打开：http://localhost:3000

---

## 🖥️ Linux/Mac 用户

### 启动服务

**终端 1 - 启动后端**：
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
uvicorn src.app:app --port 8000
```

**终端 2 - 启动前端**：
```bash
cd frontend
python -m http.server 3000
```

然后访问：http://localhost:3000

---

## 📖 项目功能

- 🎭 **多角色对话**：李白、孔子、爱因斯坦等历史人物
- 🗣️ **语音交互**：支持语音输入和语音输出
- 🎨 **3D 模型**：自动生成 3D 历史人物形象
- 👄 **口型同步**：AI 生成口型动画
- 💬 **实时对话**：WebSocket 流式对话

---

## 📚 详细文档

- [完整部署指南](./docs/LOCAL_DEPLOYMENT.md)
- [API 文档](./docs/API.md)
- [常见问题](./docs/FAQ.md)

---

## 🐛 遇到问题？

### Windows 乱码问题
- 脚本已自动设置 UTF-8 编码（chcp 65001）
- 如果仍然乱码，右键命令行窗口 → 属性 → 字体 → 选择支持中文的字体

### 端口被占用
- 修改 `auto_start.bat` 中的端口号（8000、3000）

### 依赖安装失败
- 使用 `uv sync` 而非 `pip install`
- 或使用国内镜像：`pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
