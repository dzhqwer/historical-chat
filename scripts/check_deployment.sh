#!/bin/bash

# 本地部署检查脚本

echo "======================================"
echo "  历史人物对话系统 - 本地部署检查"
echo "======================================"
echo ""

# 检查 Python 版本
echo "1. 检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "   ✅ Python 版本: $PYTHON_VERSION"

    # 检查版本是否 >= 3.9
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 9 ]; then
        echo "   ✅ Python 版本满足要求 (>= 3.9)"
    else
        echo "   ❌ Python 版本过低，需要 3.9 或更高版本"
        exit 1
    fi
else
    echo "   ❌ 未找到 Python 3"
    exit 1
fi

# 检查端口占用
echo ""
echo "2. 检查端口占用..."
check_port() {
    PORT=$1
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "   ⚠️  端口 $PORT 已被占用"
        lsof -Pi :$PORT -sTCP:LISTEN | grep LISTEN
        return 1
    else
        echo "   ✅ 端口 $PORT 可用"
        return 0
    fi
}

PORT_8000_OK=true
PORT_3000_OK=true

check_port 8000 || PORT_8000_OK=false
check_port 3000 || PORT_3000_OK=false

if [ "$PORT_8000_OK" = false ] || [ "$PORT_3000_OK" = false ]; then
    echo ""
    echo "   💡 提示: 可以使用其他端口启动服务"
    echo "      后端: python -m uvicorn src.app:app --port 8080"
    echo "      前端: python -m http.server 8080"
fi

# 检查必要文件
echo ""
echo "3. 检查项目文件..."
check_file() {
    FILE=$1
    if [ -f "$FILE" ]; then
        echo "   ✅ $FILE"
        return 0
    else
        echo "   ❌ $FILE (缺失)"
        return 1
    fi
}

MISSING_FILES=0

check_file "src/app.py" || MISSING_FILES=$((MISSING_FILES + 1))
check_file "src/agents/agent.py" || MISSING_FILES=$((MISSING_FILES + 1))
check_file "config/agent_llm_config.json" || MISSING_FILES=$((MISSING_FILES + 1))
check_file "assets/historical_figures.json" || MISSING_FILES=$((MISSING_FILES + 1))
check_file "frontend/index.html" || MISSING_FILES=$((MISSING_FILES + 1))

if [ $MISSING_FILES -gt 0 ]; then
    echo ""
    echo "   ❌ 发现 $MISSING_FILES 个文件缺失"
    echo "   💡 请确保所有项目文件都已下载"
    exit 1
fi

# 检查依赖
echo ""
echo "4. 检查依赖..."
if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt 存在"

    # 检查 uv
    if command -v uv &> /dev/null; then
        echo "   ✅ uv 已安装 (推荐)"
        INSTALL_METHOD="uv"
    elif command -v pip3 &> /dev/null; then
        echo "   ✅ pip3 已安装"
        INSTALL_METHOD="pip"
    else
        echo "   ❌ 未找到 uv 或 pip3"
        echo "   💡 请安装: https://docs.python.org/3/installing/"
        exit 1
    fi
else
    echo "   ❌ requirements.txt 不存在"
    exit 1
fi

# 安装依赖
echo ""
echo "5. 安装依赖..."
if [ "$INSTALL_METHOD" = "uv" ]; then
    echo "   使用 uv 安装依赖..."
    uv sync
elif [ "$INSTALL_METHOD" = "pip" ]; then
    echo "   使用 pip 安装依赖..."
    pip3 install -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo "   ✅ 依赖安装成功"
else
    echo "   ❌ 依赖安装失败"
    exit 1
fi

# 显示部署信息
echo ""
echo "======================================"
echo "  ✅ 检查通过！可以开始部署"
echo "======================================"
echo ""
echo "📋 下一步操作:"
echo ""
echo "1️⃣  启动后端服务:"
echo "   cd $(pwd)"
if [ "$PORT_8000_OK" = false ]; then
    echo "   python -m uvicorn src.app:app --port 8080"
else
    echo "   python -m uvicorn src.app:app --port 8000"
fi
echo ""
echo "2️⃣  启动前端服务（新终端）:"
echo "   cd $(pwd)/frontend"
if [ "$PORT_3000_OK" = false ]; then
    echo "   python -m http.server 8080"
else
    echo "   python -m http.server 3000"
fi
echo ""
echo "3️⃣  打开浏览器访问:"
if [ "$PORT_3000_OK" = false ]; then
    echo "   http://localhost:8080"
else
    echo "   http://localhost:3000"
fi
echo ""
echo "📚 详细文档: docs/LOCAL_DEPLOYMENT.md"
echo ""
