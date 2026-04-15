@echo off
REM ========================================
REM 自动启动后端和前端服务
REM ========================================

chcp 65001 >nul 2>&1

cls
echo.
echo ========================================
echo   历史人物对话系统 - 自动启动
echo ========================================
echo.

cd /d "%~dp0.."

set PYTHONPATH=%PYTHONPATH%;%CD%\src

REM 检查端口是否被占用
netstat -ano | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo [警告] 端口 8000 已被占用
    echo 请先关闭占用该端口的程序，或修改启动命令中的端口号
    pause
    exit /b 1
)

netstat -ano | findstr ":3000" >nul 2>&1
if not errorlevel 1 (
    echo [警告] 端口 3000 已被占用
    echo 请先关闭占用该端口的程序，或修改启动命令中的端口号
    pause
    exit /b 1
)

echo [信息] 正在启动后端服务 (端口 8000)...
start "后端服务" cmd /k "uvicorn src.app:app --port 8000"

echo [信息] 等待后端服务启动...
timeout /t 3 /nobreak >nul

echo [信息] 正在启动前端服务 (端口 3000)...
start "前端服务" cmd /k "cd frontend && python -m http.server 3000"

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo 后端服务: http://localhost:8000
echo 前端界面: http://localhost:3000
echo API 文档: http://localhost:8000/docs
echo.
echo [提示] 请在浏览器中打开 http://localhost:3000
echo [提示] 关闭服务时，关闭打开的两个命令行窗口即可
echo.

pause
