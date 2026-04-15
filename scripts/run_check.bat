@echo off
REM 启动器 - 确保窗口不会关闭

REM 切换到 UTF-8 编码，解决中文乱码问题
chcp 65001 >nul 2>&1

echo 正在启动检查脚本...
echo.

REM 调用检查脚本
call "%~dp0check_deployment_safe.bat"

REM 确保窗口不会关闭
echo.
echo ======================================
echo   按任意键关闭此窗口...
echo ======================================
pause >nul
