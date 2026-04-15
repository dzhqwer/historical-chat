@echo off
REM ========================================
REM Python 环境诊断脚本
REM ========================================

chcp 65001 >nul 2>&1

cls
echo.
echo ========================================
echo   Python 环境诊断工具
echo ========================================
echo.

cd /d "%~dp0.."

set PYTHON_OK=0
set PIP_OK=0
set UV_OK=0

echo [1] 检查 Python 安装...
where python >nul 2>&1
if errorlevel 1 (
    echo [失败] 未找到 Python 命令
    echo.
    echo 请下载并安装 Python:
    echo https://www.python.org/downloads/
    echo.
    echo ⚠️ 安装时务必勾选 "Add Python to PATH"
    echo.
    goto :end
) else (
    echo [通过] 找到 Python
    python --version
    set PYTHON_OK=1
)

echo.
echo [2] 检查 Python 版本...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 版本: %PYTHON_VERSION%

REM 解析主版本号
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo [失败] Python 版本过低，需要 3.9 或更高版本
    goto :end
)

if %MAJOR% EQU 3 (
    if %MINOR% LSS 9 (
        echo [失败] Python 版本过低，需要 3.9 或更高版本
        goto :end
    )
)

echo [通过] Python 版本符合要求 (>= 3.9)

echo.
echo [3] 检查 pip...
where pip >nul 2>&1
if errorlevel 1 (
    echo [失败] 未找到 pip
    echo 尝试修复: python -m ensurepip
) else (
    echo [通过] 找到 pip
    pip --version
    set PIP_OK=1
)

echo.
echo [4] 检查环境变量...
if defined PYTHONPATH (
    echo [信息] PYTHONPATH 已设置
    echo       值: %PYTHONPATH%
) else (
    echo [警告] PYTHONPATH 未设置
)

echo.
echo [5] 测试 Python 导入...
echo 尝试导入 sys...
python -c "import sys; print(f'Python 路径: {sys.executable}')" 2>nul
if errorlevel 1 (
    echo [失败] Python 无法正常工作
) else (
    echo [通过] Python 导入正常
)

echo.
echo [6] 检查已安装的关键包...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [失败] fastapi 未安装
) else (
    echo [通过] fastapi 已安装
)

python -c "import langchain" 2>nul
if errorlevel 1 (
    echo [失败] langchain 未安装
) else (
    echo [通过] langchain 已安装
)

python -c "import langgraph" 2>nul
if errorlevel 1 (
    echo [失败] langgraph 未安装
) else (
    echo [通过] langgraph 已安装
)

python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo [失败] uvicorn 未安装
) else (
    echo [通过] uvicorn 已安装
)

echo.
echo [7] 检查 uv 包管理器...
where uv >nul 2>&1
if errorlevel 1 (
    echo [警告] uv 未安装
    echo 是否现在安装 uv? (Y/N)
    choice /c YN /n
    if errorlevel 2 (
        echo 跳过安装
    ) else (
        echo 正在安装 uv...
        pip install uv
        if errorlevel 1 (
            echo [失败] uv 安装失败
        ) else (
            echo [成功] uv 安装成功
            set UV_OK=1
        )
    )
) else (
    echo [通过] uv 已安装
    uv --version
    set UV_OK=1
)

echo.
echo ========================================
echo   诊断完成
echo ========================================
echo.

if %PYTHON_OK% EQU 1 (
    if %UV_OK% EQU 1 (
        echo ✅ 环境就绪，可以运行: scripts\auto_start.bat
    ) else (
        echo ⚠️ 需要手动安装依赖
        echo    运行: pip install -r requirements.txt
    )
) else (
    echo ❌ 需要先安装 Python
    echo    下载: https://www.python.org/downloads/
)

echo.
echo 诊断结果已保存
pause

:end
