@echo off
REM 本地部署检查脚本 (Windows - 安全版本)
REM 此版本会记录日志并防止窗口自动关闭

REM 切换到 UTF-8 编码，解决中文乱码问题
chcp 65001 >nul 2>&1

echo ======================================
echo   历史人物对话系统 - 本地部署检查
echo ======================================
echo.

REM 创建日志文件
set LOG_FILE=%TEMP%\deployment_check_%RANDOM%.txt
echo 检查开始时间: %date% %time% > "%LOG_FILE%"

REM 设置错误处理
if "%ERRORSCRIPT%"=="" (
    set ERRORSCRIPT=call :error_handler
)

goto :main

:error_handler
echo.
echo ======================================
echo   [错误] 脚本执行出错
echo ======================================
echo.
echo 错误发生在: %1
echo 错误代码: %errorlevel%
echo.
echo 详细日志已保存到: %LOG_FILE%
echo.
echo 请检查:
echo 1. Python 是否正确安装
echo 2. 是否在项目根目录运行此脚本
echo 3. 所有项目文件是否完整
echo.
pause
exit /b %errorlevel%

:main
REM 检查是否在项目根目录
if not exist "src\app.py" (
    echo [错误] 未找到 src\app.py
    echo [提示] 请确保在项目根目录运行此脚本
    echo.
    echo 当前目录: %cd%
    echo.
    pause
    exit /b 1
)

REM 检查 Python 版本
echo 1. 检查 Python 版本...
python --version >> "%LOG_FILE%" 2>&1
if %errorlevel% neq 0 (
    echo    [错误] 未找到 Python
    echo    [提示] 请安装 Python 3.9 或更高版本
    echo    下载地址: https://www.python.org/downloads/
    echo    注意: 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo    [成功] Python 版本: %PYTHON_VERSION%
    echo    Python 版本: %PYTHON_VERSION% >> "%LOG_FILE%"
)

REM 检查端口占用
echo.
echo 2. 检查端口占用...
echo 检查端口 8000 >> "%LOG_FILE%"
netstat -ano | findstr :8000 >> "%LOG_FILE%" 2>&1
if %errorlevel% equ 0 (
    echo    [警告] 端口 8000 已被占用
    netstat -ano | findstr :8000
    echo 端口 8000 占用信息 >> "%LOG_FILE%"
    set PORT_8000_OK=false
) else (
    echo    [成功] 端口 8000 可用
    echo 端口 8000 可用 >> "%LOG_FILE%"
    set PORT_8000_OK=true
)

echo 检查端口 3000 >> "%LOG_FILE%"
netstat -ano | findstr :3000 >> "%LOG_FILE%" 2>&1
if %errorlevel% equ 0 (
    echo    [警告] 端口 3000 已被占用
    netstat -ano | findstr :3000
    echo 端口 3000 占用信息 >> "%LOG_FILE%"
    set PORT_3000_OK=false
) else (
    echo    [成功] 端口 3000 可用
    echo 端口 3000 可用 >> "%LOG_FILE%"
    set PORT_3000_OK=true
)

REM 检查必要文件
echo.
echo 3. 检查项目文件...
set MISSING_FILES=0

if exist "src\app.py" (
    echo    [成功] src\app.py
    echo src\app.py 存在 >> "%LOG_FILE%"
) else (
    echo    [错误] src\app.py (缺失)
    echo src\app.py 缺失 >> "%LOG_FILE%"
    set /a MISSING_FILES+=1
)

if exist "src\agents\agent.py" (
    echo    [成功] src\agents\agent.py
    echo src\agents\agent.py 存在 >> "%LOG_FILE%"
) else (
    echo    [错误] src\agents\agent.py (缺失)
    echo src\agents\agent.py 缺失 >> "%LOG_FILE%"
    set /a MISSING_FILES+=1
)

if exist "config\agent_llm_config.json" (
    echo    [成功] config\agent_llm_config.json
    echo config\agent_llm_config.json 存在 >> "%LOG_FILE%"
) else (
    echo    [错误] config\agent_llm_config.json (缺失)
    echo config\agent_llm_config.json 缺失 >> "%LOG_FILE%"
    set /a MISSING_FILES+=1
)

if exist "assets\historical_figures.json" (
    echo    [成功] assets\historical_figures.json
    echo assets\historical_figures.json 存在 >> "%LOG_FILE%"
) else (
    echo    [错误] assets\historical_figures.json (缺失)
    echo assets\historical_figures.json 缺失 >> "%LOG_FILE%"
    set /a MISSING_FILES+=1
)

if exist "frontend\index.html" (
    echo    [成功] frontend\index.html
    echo frontend\index.html 存在 >> "%LOG_FILE%"
) else (
    echo    [错误] frontend\index.html (缺失)
    echo frontend\index.html 缺失 >> "%LOG_FILE%"
    set /a MISSING_FILES+=1
)

if %MISSING_FILES% gtr 0 (
    echo.
    echo    [错误] 发现 %MISSING_FILES% 个文件缺失
    echo    [提示] 请确保所有项目文件都已下载
    echo 缺失文件数: %MISSING_FILES% >> "%LOG_FILE%"
    echo.
    pause
    exit /b 1
)

REM 检查依赖文件
echo.
echo 4. 检查依赖文件...
if exist "requirements.txt" (
    echo    [成功] requirements.txt 存在
    echo requirements.txt 存在 >> "%LOG_FILE%"
) else (
    echo    [错误] requirements.txt 不存在
    echo requirements.txt 不存在 >> "%LOG_FILE%"
    echo.
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo 5. 安装依赖...
echo    正在安装依赖，这可能需要几分钟...
echo 开始安装依赖... >> "%LOG_FILE%"

REM 使用 python -m pip 更安全
python -m pip install -r requirements.txt >> "%LOG_FILE%" 2>&1
if %errorlevel% neq 0 (
    echo.
    echo    [错误] 依赖安装失败
    echo.
    echo 尝试使用 uv 安装...
    uv --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo    使用 uv 安装...
        uv sync >> "%LOG_FILE%" 2>&1
        if %errorlevel% equ 0 (
            echo    [成功] 依赖安装成功 (使用 uv)
            echo 依赖安装成功 (使用 uv) >> "%LOG_FILE%"
            goto :install_success
        )
    )
    echo.
    echo    [错误] 依赖安装失败
    echo    日志文件: %LOG_FILE%
    echo.
    pause
    exit /b 1
) else (
    echo    [成功] 依赖安装成功 (使用 pip)
    echo 依赖安装成功 (使用 pip) >> "%LOG_FILE%"
)

:install_success
REM 显示部署信息
echo.
echo ======================================
echo   [成功] 检查通过！可以开始部署
echo ======================================
echo.
echo 下一步操作:
echo.
echo 1. 启动后端服务:
echo    打开新的命令提示符窗口，运行:
echo.
echo    cd "%cd%"
if "%PORT_8000_OK%"=="false" (
    echo    python -m uvicorn src.app:app --port 8080
) else (
    echo    python -m uvicorn src.app:app --port 8000
)
echo.
echo 2. 启动前端服务（另一个新的命令提示符窗口）:
echo    cd "%cd%\frontend"
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
echo 详细文档:
echo    - 快速开始: docs\QUICK_START.md
echo    - 详细部署: docs\LOCAL_DEPLOYMENT.md
echo.
echo 日志文件: %LOG_FILE%
echo.
echo ======================================
echo.
pause
