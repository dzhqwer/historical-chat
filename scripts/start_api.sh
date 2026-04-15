#!/bin/bash

# 历史人物对话 API 启动脚本

echo "==================================="
echo "  历史人物对话 API 服务器"
echo "==================================="

# 检查工作目录
if [ ! -f "src/app.py" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 启动服务器
echo "启动服务器在 http://0.0.0.0:8000"
echo "API 文档: http://0.0.0.0:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

python -m uvicorn src.app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info
