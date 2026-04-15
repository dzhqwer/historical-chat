@echo off
REM 本地部署检查脚本 (Windows)

echo ======================================
echo   历史人物对话系统 - 本地部署检查
echo ======================================
echo.

REM 检查 Python 版本
echo 1. 检查 Python 版本...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    [错误] 未找到 Python
    echo    [提示] 请安装 Python 3.9 或更高版本: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    [成功] Python 版本: %PYTHON_VERSION%

REM 检查端口占用
echo.
echo 2. 检查端口占用...

netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo    [警告] 端口 8000 已被占用
    netstat -ano | findstr :8000
    set PORT_8000_OK=false
) else (
    echo    [成功] 端口 8000 可用
    set PORT_8000_OK=true
)

netstat -ano | findstr :3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo    [警告] 端口 3000 已被占用
    netstat -ano | findstr :3000
    set PORT_3000_OK=false
) else (
    echo    [成功] 端口 3000 可用
    set PORT_3000_OK=true
)

REM 检查必要文件
echo.
echo 3. 检查项目文件...

set MISSING_FILES=0

if exist "src\app.py" (
    echo    [成功] src\app.py
) else (
    echo    [错误] src\app.py (缺失)
    set /a MISSING_FILES+=1
)

if exist "src\agents\agent.py" (
    echo    [成功] src\agents\agent.py
) else (
    echo    [错误] src\agents\agent.py (缺失)
    set /a MISSING_FILES+=1
)

if exist "config\agent_llm_config.json" (
    echo    [成功] config\agent_llm_config.json
) else (
    echo    [错误] config\agent_llm_config.json (缺失)
    set /a MISSING_FILES+=1
)

if exist "assets\historical_figures.json" (
    echo    [成功] assets\historical_figures.json
) else (
    echo    [错误] assets\historical_figures.json (缺失)
    set /a MISSING_FILES+=1
)

if exist "frontend\index.html" (
    echo    [成功] frontend\index.html
) else (
    echo    [错误] frontend\index.html (缺失)
    set /a MISSING_FILES+=1
)

if %MISSING_FILES% gtr 0 (
    echo.
    echo    [错误] 发现 %MISSING_FILES% 个文件缺失
    echo    [提示] 请确保所有项目文件都已下载
    pause
    exit /b 1
)

REM 检查依赖文件
echo.
echo 4. 检查依赖文件...
if exist "requirements.txt" (
    echo    [成功] requirements.txt 存在
) else (
    echo    [错误] requirements.txt 不存在
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo 5. 安装依赖...
echo    正在安装依赖，请稍候...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo    [错误] 依赖安装失败
    pause
    exit /b 1
)
echo    [成功] 依赖安装成功

REM 显示部署信息
echo.
echo ======================================
echo   [成功] 检查通过！可以开始部署
echo ======================================
echo.
echo 下一步操作:
echo.
echo 1. 启动后端服务:
echo    cd %cd%
if "%PORT_8000_OK%"=="false" (
    echo    python -m uvicorn src.app:app --port 8080
) else (
    echo    python -m uvicorn src.app:app --port 8000
)
echo.
echo 2. 启动前端服务（新终端）:
echo    cd %cd%\frontend
if "%PORT_3000_OK%"=="false" (
    echo    python -m http.server 8080
) else (
    echo    python -m http.server 3000
)
echo.
echo 3. 打开浏览器访问:
if "%PORT_3000_OK%"=="false" (
    echo    http://localhost:8080
) else (
    echo    http://localhost:3000
)
echo.
echo 详细文档: docs\LOCAL_DEPLOYMENT.md
echo.
pause
