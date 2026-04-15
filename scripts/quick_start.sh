#!/bin/bash

# 快速启动脚本（单终端模式）

echo "======================================"
echo "  历史人物对话系统 - 快速启动"
echo "======================================"
echo ""

# 检查当前目录
if [ ! -f "src/app.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 设置环境变量
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 启动后端
echo "🚀 启动后端服务..."
echo "   地址: http://localhost:8000"
echo "   文档: http://localhost:8000/docs"
echo ""

python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
echo ""
echo "⏳ 等待后端服务就绪..."
sleep 3

# 测试后端
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 后端服务正常运行"
else
    echo "❌ 后端服务启动失败"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "======================================"
echo "  📱 前端启动"
echo "======================================"
echo ""
echo "请在另一个终端运行以下命令启动前端:"
echo ""
echo "  cd $(pwd)/frontend"
echo "  python -m http.server 3000"
echo ""
echo "然后打开浏览器访问: http://localhost:3000"
echo ""
echo "======================================"
echo ""
echo "💡 提示:"
echo "   - 后端服务正在后台运行"
echo "   - 按 Ctrl+C 停止后端服务"
echo "   - 详细文档: docs/LOCAL_DEPLOYMENT.md"
echo ""

# 等待用户中断
trap "echo ''; echo '正在停止服务...'; kill $BACKEND_PID 2>/dev/null; exit 0" INT TERM

wait
