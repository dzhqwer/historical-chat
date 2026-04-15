# ⚡ 三步快速启动

## 🔍 第一步：检查环境

运行诊断脚本：
```batch
scripts\diagnose_python.bat
```

查看输出结果，如果有 ❌ 标记，继续第二步修复。

---

## 🔧 第二步：修复问题

如果第一步发现问题，运行修复脚本：
```batch
scripts\fix_python.bat
```

根据提示选择修复选项：
- **[1]** 重新安装所有依赖（推荐）
- **[2]** 仅安装缺失的依赖
- **[3]** 使用 pip 安装（如果 uv 失败）

---

## 🚀 第三步：启动服务

修复完成后，启动服务：
```batch
scripts\auto_start.bat
```

然后在浏览器访问：**http://localhost:3000**

---

## ❓ 遇到问题？

### 如果第一步显示 "未找到 Python"

1. 下载安装 Python：https://www.python.org/downloads/
2. 安装时务必勾选 "Add Python to PATH"
3. 安装完成后重新运行第一步

### 如果第二步显示 "安装失败"

**手动安装依赖**：
```batch
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 如果第三步显示 "端口被占用"

查看并关闭占用端口的程序：
```batch
netstat -ano | findstr ":8000"
netstat -ano | findstr ":3000"
```

---

## 📚 详细文档

- [Python 问题排查](./docs/PYTHON_TROUBLESHOOTING.md) - 详细的问题诊断和解决方案
- [快速参考](./QUICK_REFERENCE.md) - 常用命令和配置
- [API 文档](./docs/API.md) - 后端接口说明

---

## 💡 提示

- 使用 `py` 命令代替 `python`（如果 py 可用）
- 使用国内镜像加速下载
- 以管理员身份运行命令提示符（如果遇到权限问题）
- 关闭杀毒软件（如果阻止安装）
