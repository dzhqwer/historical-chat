@echo off
REM ========================================
REM 历史人物对话系统 - Windows 快速启动
REM ========================================

REM 切换到 UTF-8 编码
chcp 65001 >nul 2>&1

cls
echo.
echo ========================================
echo   历史人物对话系统 - 启动中...
echo ========================================
echo.

cd /d "%~dp0.."

echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version

echo.
echo [2/4] 设置环境变量...
set PYTHONPATH=%PYTHONPATH%;%CD%\src

echo.
echo [3/4] 检查依赖...
pip show uv >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 uv 包管理器...
    pip install uv
)

echo.
echo [4/4] 同步依赖...
uv sync

echo.
echo ========================================
echo   所有检查通过！
echo ========================================
echo.
echo 现在需要启动服务：
echo.
echo 方式 A - 自动启动（推荐）：
echo   运行 scripts\auto_start.bat
echo.
echo 方式 B - 手动启动：
echo   终端 1: uvicorn src.app:app --port 8000
echo   终端 2: cd frontend ^&^& python -m http.server 3000
echo.
echo 启动后访问: http://localhost:3000
echo.

pause
