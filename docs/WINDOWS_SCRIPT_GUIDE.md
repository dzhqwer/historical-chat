# Windows 运行脚本指南

## ❌ 不要双击 .bat 文件！

双击 `.bat` 文件会导致窗口一闪而过，看不到输出内容。

## ✅ 正确的运行方式

### 方法 1：使用命令提示符（推荐）

**步骤**：

1. **打开命令提示符**
   - 按 `Win + R`
   - 输入 `cmd`
   - 按 Enter

2. **导航到项目目录**
   ```batch
   cd C:\你的项目路径\projects
   ```
   例如：
   ```batch
   cd C:\Users\你的用户名\Desktop\projects
   ```

3. **运行脚本**
   ```batch
   scripts\check_deployment_safe.bat
   ```
   或
   ```batch
   scripts\run_check.bat
   ```

4. **查看输出**
   - 窗口会保持打开，你可以看到所有输出
   - 按任意键关闭窗口

---

### 方法 2：使用 PowerShell

**步骤**：

1. **打开 PowerShell**
   - 按 `Win + X`，选择"Windows PowerShell"

2. **导航到项目目录**
   ```powershell
   cd C:\你的项目路径\projects
   ```

3. **运行脚本**
   ```powershell
   .\scripts\check_deployment_safe.bat
   ```

---

### 方法 3：创建桌面快捷方式（方便使用）

**步骤**：

1. 在桌面右键 → 新建 → 快捷方式
2. 位置输入：
   ```
   cmd /k "cd /d C:\你的项目路径\projects && scripts\check_deployment_safe.bat"
   ```
3. 命名为"部署检查"
4. 双击快捷方式即可运行

---

## 📝 可用的脚本

| 脚本 | 用途 | 推荐度 |
|------|------|--------|
| `check_deployment_safe.bat` | 环境检查和依赖安装（带日志） | ⭐⭐⭐⭐⭐ |
| `run_check.bat` | 启动器（包装 check_deployment_safe.bat） | ⭐⭐⭐⭐ |
| `check_deployment.bat` | 原始检查脚本 | ⭐⭐⭐ |

---

## 🔍 为什么脚本会关闭？

### 常见原因

1. **双击文件** - Windows 默认行为是执行完后关闭窗口
2. **遇到错误** - 脚本中间出错会提前退出
3. **Python 未安装** - 找不到 Python 命令
4. **路径错误** - 不在正确的目录运行

### 解决方法

- ✅ 在命令提示符中运行（不要双击）
- ✅ 使用 `check_deployment_safe.bat`（带日志和错误处理）
- ✅ 检查 Python 是否正确安装
- ✅ 确保在项目根目录运行

---

## 🛠️ 如果还是看不到输出

### 查看日志文件

安全版本会生成日志文件，位置会在输出中显示：

```
日志文件: C:\Users\你的用户名\AppData\Local\Temp\deployment_check_xxxxx.txt
```

**打开日志文件**：
1. 复制日志文件路径
2. 按 `Win + R`
3. 粘贴路径并按 Enter
4. 用记事本打开查看

---

## 📋 手动检查（如果脚本失败）

如果脚本无法运行，可以手动执行以下步骤：

### 1. 检查 Python

```batch
python --version
```

应该看到类似：`Python 3.9.0`

如果看到"不是内部或外部命令"，说明 Python 未安装或未添加到 PATH。

### 2. 安装依赖

```batch
cd 你的项目路径\projects
pip install -r requirements.txt
```

### 3. 启动后端

```batch
python -m uvicorn src.app:app --port 8000
```

### 4. 启动前端（新窗口）

```batch
cd 你的项目路径\projects\frontend
python -m http.server 3000
```

---

## ❓ 遇到问题

### 脚本窗口还是一闪而过？

**解决方案**：
1. 不要双击 `.bat` 文件
2. 使用命令提示符运行（见方法 1）
3. 或者使用 `run_check.bat` 启动器

### 找不到 Python？

**解决方案**：
1. 下载安装 Python：https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 重启命令提示符

### 权限被拒绝？

**解决方案**：
1. 右键命令提示符 → 以管理员身份运行
2. 或关闭杀毒软件重试

---

## 📞 获取帮助

如果以上方法都不行：

1. **查看详细文档**：`docs\LOCAL_DEPLOYMENT.md`
2. **查看日志文件**：查看生成的日志文件
3. **手动部署**：参考"手动检查"部分

---

**记住：不要双击 .bat 文件！使用命令提示符运行！** 💡
