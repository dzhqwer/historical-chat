# 🐛 Python 环境问题排查

## 常见问题

### ❌ 问题 1：未找到 Python

**症状**：
```
'python' 不是内部或外部命令
```

**解决方案**：

1. **检查是否安装了 Python**
   ```batch
   python --version
   ```
   或
   ```batch
   py --version
   ```

2. **如果未安装，下载安装**
   - 访问：https://www.python.org/downloads/
   - 下载 Python 3.9 或更高版本
   - ⚠️ **重要**：安装时务必勾选 "Add Python to PATH"

3. **如果已安装但无法识别**
   - 找到 Python 安装路径（通常是 `C:\Python3x\`）
   - 将 Python 路径添加到系统环境变量

---

### ❌ 问题 2：Python 版本过低

**症状**：
```
Python 3.7.x 或更低版本
```

**解决方案**：

1. 卸载旧版本 Python
2. 下载安装 Python 3.9+：
   - https://www.python.org/downloads/
   - 推荐版本：Python 3.10 或 3.11

---

### ❌ 问题 3：依赖包安装失败

**症状**：
```
ModuleNotFoundError: No module named 'fastapi'
```

**解决方案**：

#### 方案 A：使用诊断和修复脚本

```batch
# 运行诊断
scripts\diagnose_python.bat

# 运行修复
scripts\fix_python.bat
```

#### 方案 B：手动安装

```batch
# 使用 pip 安装
pip install -r requirements.txt

# 或使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 方案 C：逐个安装

```batch
pip install fastapi uvicorn
pip install langchain langchain-openai
pip install langgraph
pip install openai aiohttp websockets
pip install coze-coding-dev-sdk
```

---

### ❌ 问题 4：uv 命令不存在

**症状**：
```
'uv' 不是内部或外部命令
```

**解决方案**：

```batch
# 安装 uv
pip install uv

# 或使用国内镜像
pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple
```

然后重新运行：
```batch
uv sync
```

---

### ❌ 问题 5：SSL 证书错误

**症状**：
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**解决方案**：

使用国内镜像源：

```batch
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

---

### ❌ 问题 6：权限不足

**症状**：
```
Permission denied
Access is denied
```

**解决方案**：

**选项 1**：以管理员身份运行命令提示符

**选项 2**：使用用户安装
```batch
pip install --user -r requirements.txt
```

**选项 3**：临时禁用 UAC（不推荐）

---

## 🔍 快速诊断

运行诊断脚本检查所有问题：

```batch
scripts\diagnose_python.bat
```

诊断脚本会检查：
- ✅ Python 是否安装
- ✅ Python 版本是否符合要求
- ✅ pip 是否可用
- ✅ 环境变量是否配置
- ✅ 关键依赖包是否安装
- ✅ uv 包管理器是否可用

---

## 🔧 一键修复

运行修复脚本自动解决常见问题：

```batch
scripts\fix_python.bat
```

修复脚本支持：
- 重新安装所有依赖
- 仅安装缺失的依赖
- 使用 pip 代替 uv
- 手动指定 Python 路径

---

## 📋 手动检查步骤

### 1. 检查 Python

```batch
python --version
# 或
py --version
```

### 2. 检查 pip

```batch
pip --version
```

### 3. 检查已安装的包

```batch
pip list
```

查找以下关键包：
- fastapi
- uvicorn
- langchain
- langgraph
- openai
- aiohttp

### 4. 检查环境变量

```batch
echo %PATH%
echo %PYTHONPATH%
```

---

## 💡 常用命令

```batch
# 升级 pip
python -m pip install --upgrade pip

# 清理 pip 缓存
pip cache purge

# 查看包信息
pip show fastapi

# 卸载包
pip uninstall fastapi

# 查看依赖树
pip install pipdeptree
pipdeptree
```

---

## 🆘 仍然无法解决？

### 收集诊断信息

```batch
# 保存到文件
python --version > diagnostic.txt
pip --version >> diagnostic.txt
pip list >> diagnostic.txt
echo %PATH% >> diagnostic.txt
echo %PYTHONPATH% >> diagnostic.txt
```

### 常见 Python 安装路径

- `C:\Python39\`
- `C:\Python310\`
- `C:\Python311\`
- `C:\Users\你的用户名\AppData\Local\Programs\Python\Python3x\`

### 推荐的国内镜像源

```
清华: https://pypi.tuna.tsinghua.edu.cn/simple
阿里: https://mirrors.aliyun.com/pypi/simple/
豆瓣: https://pypi.doubanio.com/simple/
```

---

## ✅ 验证环境

安装完成后，运行以下命令验证：

```batch
python -c "import fastapi; print('✅ fastapi')"
python -c "import langchain; print('✅ langchain')"
python -c "import langgraph; print('✅ langgraph')"
python -c "import uvicorn; print('✅ uvicorn')"
python -c "import openai; print('✅ openai')"
```

如果所有命令都显示 ✅，说明环境配置成功！

然后可以启动服务：
```batch
scripts\auto_start.bat
```
