#!/bin/bash
# 项目打包脚本

echo "========================================="
echo "  历史人物对话系统 - 项目打包"
echo "========================================="
echo ""

PROJECT_ROOT="/workspace/projects"
OUTPUT_DIR="/workspace/projects/dist"
PACKAGE_NAME="historical-chat-project"
PACKAGE_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}.tar.gz"

# 清理旧输出
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# 创建临时目录
TEMP_DIR="${OUTPUT_DIR}/${PACKAGE_NAME}"
mkdir -p "$TEMP_DIR"

echo "正在打包文件..."
echo ""

# 复制配置文件
echo "📁 配置文件..."
cp -r "${PROJECT_ROOT}/config" "$TEMP_DIR/"
cp -r "${PROJECT_ROOT}/assets" "$TEMP_DIR/"

# 复制源代码
echo "📁 源代码..."
cp -r "${PROJECT_ROOT}/src" "$TEMP_DIR/"

# 复制前端
echo "📁 前端..."
cp -r "${PROJECT_ROOT}/frontend" "$TEMP_DIR/"

# 复制依赖文件
echo "📁 依赖文件..."
cp "${PROJECT_ROOT}/requirements.txt" "$TEMP_DIR/"
cp "${PROJECT_ROOT}/pyproject.toml" "$TEMP_DIR/"

# 复制文档
echo "📁 文档..."
cp "${PROJECT_ROOT}/README.md" "$TEMP_DIR/"
cp "${PROJECT_ROOT}/LOCAL_SETUP.md" "$TEMP_DIR/"
cp "${PROJECT_ROOT}/QUICK_LOCAL_START.md" "$TEMP_DIR/"

# 创建启动脚本
echo "📁 启动脚本..."
cat > "$TEMP_DIR/start.bat" << 'STARTBAT'
@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   历史人物对话系统 - 启动脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装
    pause
    exit /b 1
)

echo [1/2] 启动后端服务...
start "后端服务" cmd /k "set PYTHONPATH=%PYTHONPATH%;%CD%\src && uvicorn src.app:app --host 0.0.0.0 --port 8000"

echo [2/2] 等待 3 秒后启动前端...
timeout /t 3 /nobreak >nul

start "前端服务" cmd /k "cd frontend && python -m http.server 3000"

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo 后端: http://localhost:8000
echo 前端: http://localhost:3000
echo.
echo 在浏览器中打开: http://localhost:3000
echo.

pause
STARTBAT

cat > "$TEMP_DIR/start.sh" << 'STARTSH'
#!/bin/bash
echo "========================================="
echo "  历史人物对话系统 - 启动脚本"
echo "========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装"
    exit 1
fi

echo "[1/2] 启动后端服务..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
uvicorn src.app:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "[2/2] 启动前端服务..."
cd frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "========================================="
echo "  启动完成！"
echo "========================================="
echo ""
echo "后端: http://localhost:8000"
echo "前端: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

wait $BACKEND_PID $FRONTEND_PID
STARTSH

chmod +x "$TEMP_DIR/start.sh"

# 创建安装脚本
cat > "$TEMP_DIR/install.bat" << 'INSTALLBAT'
@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   历史人物对话系统 - 安装依赖
echo ========================================
echo.

echo 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version

echo.
echo 安装依赖包...
echo.

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败
    echo.
    echo 尝试手动安装：
    echo pip install fastapi uvicorn langchain langchain-openai langgraph openai aiohttp websockets coze-coding-dev-sdk
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 现在可以运行 start.bat 启动服务
echo.

pause
INSTALLBAT

cat > "$TEMP_DIR/install.sh" << 'INSTALLSH'
#!/bin/bash
echo "========================================="
echo "  历史人物对话系统 - 安装依赖"
echo "========================================="
echo ""

echo "检查 Python..."
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[错误] 未找到 Python"
    echo "请先安装 Python: https://www.python.org/downloads/"
    exit 1
fi

python3 --version

echo ""
echo "安装依赖包..."
echo ""

pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 依赖安装失败"
    echo ""
    echo "尝试手动安装："
    echo "pip install fastapi uvicorn langchain langchain-openai langgraph openai aiohttp websockets coze-coding-dev-sdk"
    echo ""
    exit 1
fi

echo ""
echo "========================================="
echo "  安装完成！"
echo "========================================="
echo ""
echo "现在可以运行 ./start.sh 启动服务"
echo ""
INSTALLSH

chmod +x "$TEMP_DIR/install.sh"

# 创建说明文件
cat > "$TEMP_DIR/README.txt" << 'README'
========================================
历史人物对话系统
========================================

快速开始：

1. 安装依赖
   Windows: 双击 install.bat
   Linux/Mac: chmod +x install.sh && ./install.sh

2. 启动服务
   Windows: 双击 start.bat
   Linux/Mac: chmod +x start.sh && ./start.sh

3. 访问应用
   浏览器打开: http://localhost:3000

详细文档：
- QUICK_LOCAL_START.md - 快速开始指南
- LOCAL_SETUP.md - 完整部署指南
- README.md - 项目说明

停止服务：
- 在对应的命令行窗口按 Ctrl+C

========================================
README

echo ""
echo "正在压缩..."
cd "$OUTPUT_DIR"
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"

# 计算 MD5
echo ""
echo "校验信息："
echo "文件名: ${PACKAGE_NAME}.tar.gz"
echo "大小: $(du -h "${PACKAGE_NAME}.tar.gz" | cut -f1)"
echo "路径: ${PACKAGE_FILE}"

echo ""
echo "========================================="
echo "  打包完成！"
echo "========================================="
echo ""
echo "文件位置: ${PACKAGE_FILE}"
echo ""
echo "下载说明："
echo "1. 文件已打包完成"
echo "2. 可以通过以下方式获取："
echo "   - 从当前环境下载文件"
echo "   - 复制 /workspace/projects/dist/historical-chat-project.tar.gz"
echo ""
