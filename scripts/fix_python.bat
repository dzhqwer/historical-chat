@echo off
REM ========================================
REM Python 环境快速修复脚本
REM ========================================

chcp 65001 >nul 2>&1

cls
echo.
echo ========================================
echo   Python 环境修复工具
echo ========================================
echo.

cd /d "%~dp0.."

echo 正在检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo.
    echo 请先安装 Python:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装 Python 3.9 或更高版本
    echo 3. ⚠️ 安装时务必勾选 "Add Python to PATH"
    echo 4. 安装完成后重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo [OK] Python 已安装
python --version
echo.

echo ========================================
echo   选择修复选项
echo ========================================
echo.
echo [1] 重新安装所有依赖 (推荐)
echo [2] 仅安装缺失的依赖
echo [3] 使用 pip 安装 (代替 uv)
echo [4] 手动指定 Python 路径
echo [0] 退出
echo.

set /p CHOICE="请选择 (0-4): "

if "%CHOICE%"=="1" goto :install_all
if "%CHOICE%"=="2" goto :install_missing
if "%CHOICE%"=="3" goto :pip_install
if "%CHOICE%"=="4" goto :custom_python
if "%CHOICE%"=="0" exit /b 0

:install_all
echo.
echo 正在安装 uv 包管理器...
pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在同步项目依赖...
uv sync

if errorlevel 1 (
    echo.
    echo [错误] uv sync 失败，尝试使用 pip...
    goto :pip_install
) else (
    echo.
    echo ✅ 依赖安装成功！
    goto :success
)

:install_missing
echo.
echo 检查已安装的包...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 安装 fastapi...
    pip install fastapi uvicorn
)

python -c "import langchain" 2>nul
if errorlevel 1 (
    echo 安装 langchain...
    pip install langchain langchain-openai
)

python -c "import langgraph" 2>nul
if errorlevel 1 (
    echo 安装 langgraph...
    pip install langgraph
)

python -c "import openai" 2>nul
if errorlevel 1 (
    echo 安装 openai...
    pip install openai
)

python -c "import aiohttp" 2>nul
if errorlevel 1 (
    echo 安装 aiohttp...
    pip install aiohttp
)

echo.
echo ✅ 缺失依赖已安装！
goto :success

:pip_install
echo.
echo 使用 pip 安装所有依赖...
echo.

echo [1/5] 安装 fastapi...
pip install fastapi uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple

echo [2/5] 安装 langchain...
pip install langchain langchain-openai -i https://pypi.tuna.tsinghua.edu.cn/simple

echo [3/5] 安装 langgraph...
pip install langgraph -i https://pypi.tuna.tsinghua.edu.cn/simple

echo [4/5] 安装其他依赖...
pip install openai aiohttp websockets python-multipart -i https://pypi.tuna.tsinghua.edu.cn/simple

echo [5/5] 安装 coze SDK...
pip install coze-coding-dev-sdk -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ✅ 依赖安装完成！
goto :success

:custom_python
echo.
echo 请输入 Python 的完整路径
echo 例如: C:\Python39\python.exe
set /p PYTHON_PATH="Python 路径: "

if not exist "%PYTHON_PATH%" (
    echo [错误] 路径不存在: %PYTHON_PATH%
    pause
    exit /b 1
)

echo.
echo 设置 Python 路径为: %PYTHON_PATH%
echo.

REM 临时设置 Python
set PATH=%PATH%;%~dp0..

REM 测试
"%PYTHON_PATH%" --version
if errorlevel 1 (
    echo [错误] Python 无法运行
    pause
    exit /b 1
)

echo.
echo ✅ Python 配置成功！
goto :success

:success
echo.
echo ========================================
echo   修复完成
echo ========================================
echo.
echo 现在可以启动服务了：
echo   scripts\auto_start.bat
echo.
echo 或手动启动：
echo   终端 1: uvicorn src.app:app --port 8000
echo   终端 2: cd frontend ^&^& python -m http.server 3000
echo.

pause
