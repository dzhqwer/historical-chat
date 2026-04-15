#!/bin/bash

# 历史人物对话系统 - 完整启动脚本

echo "==================================="
echo "  历史人物沉浸式对话系统"
echo "==================================="
echo ""

# 检查是否在项目根目录
if [ ! -f "src/app.py" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 启动后端服务
echo "🚀 启动后端 API 服务..."
echo "   API 地址: http://localhost:8000"
echo "   API 文档: http://localhost:8000/docs"
echo ""

python -m uvicorn src.app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload &
BACKEND_PID=$!

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 启动前端服务
echo ""
echo "🎨 启动前端服务..."
echo "   前端地址: http://localhost:3000"
echo ""

cd frontend
python -m http.server 3000 &
FRONTEND_PID=$!

cd ..

# 显示访问信息
echo ""
echo "==================================="
echo "  ✅ 服务已启动"
echo "==================================="
echo ""
echo "📱 访问地址:"
echo "   前端界面: http://localhost:3000"
echo "   后端 API: http://localhost:8000"
echo "   API 文档: http://localhost:8000/docs"
echo ""
echo "💡 使用说明:"
echo "   1. 在浏览器中打开 http://localhost:3000"
echo "   2. 点击'切换人物'选择历史人物"
echo "   3. 输入消息开始对话"
echo "   4. 点击'播放语音'听 AI 回复"
echo ""
echo "⏹️  停止服务: 按 Ctrl+C"
echo ""
echo "==================================="

# 等待用户中断
trap "echo ''; echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

wait
