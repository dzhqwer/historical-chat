@echo off
REM ========================================
REM 功能测试脚本
REM ========================================

chcp 65001 >nul 2>&1

cls
echo.
echo ========================================
echo   历史人物对话系统 - 功能测试
echo ========================================
echo.

cd /d "%~dp0.."

REM 测试 1: 检查 Python 环境
echo [测试 1/5] Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [失败] 未找到 Python
) else (
    echo [通过] Python 已安装
    python --version
)

REM 测试 2: 检查依赖
echo.
echo [测试 2/5] Python 依赖...
pip show uvicorn >nul 2>&1
if errorlevel 1 (
    echo [失败] uvicorn 未安装
) else (
    echo [通过] uvicorn 已安装
)

pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [失败] fastapi 未安装
) else (
    echo [通过] fastapi 已安装
)

pip show langchain >nul 2>&1
if errorlevel 1 (
    echo [失败] langchain 未安装
) else (
    echo [通过] langchain 已安装
)

REM 测试 3: 检查配置文件
echo.
echo [测试 3/5] 配置文件...
if exist "config\agent_llm_config.json" (
    echo [通过] Agent 配置文件存在
) else (
    echo [失败] Agent 配置文件不存在
)

if exist "assets\historical_figures.json" (
    echo [通过] 历史人物配置存在
) else (
    echo [失败] 历史人物配置不存在
)

REM 测试 4: 检查前端文件
echo.
echo [测试 4/5] 前端文件...
if exist "frontend\index.html" (
    echo [通过] 前端主页存在
) else (
    echo [失败] 前端主页不存在
)

if exist "frontend\avatar-3d.js" (
    echo [通过] 3D 模型组件存在
) else (
    echo [失败] 3D 模型组件不存在
)

REM 测试 5: 检查端口
echo.
echo [测试 5/5] 端口状态...
netstat -ano | findstr ":8000" >nul 2>&1
if errorlevel 1 (
    echo [通过] 端口 8000 可用
) else (
    echo [警告] 端口 8000 已被占用
)

netstat -ano | findstr ":3000" >nul 2>&1
if errorlevel 1 (
    echo [通过] 端口 3000 可用
) else (
    echo [警告] 端口 3000 已被占用
)

echo.
echo ========================================
echo   测试完成
echo ========================================
echo.
echo 如果所有测试都通过，可以运行以下命令启动：
echo   scripts\auto_start.bat
echo.

pause
