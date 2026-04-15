#!/bin/bash
# 项目文件导出脚本

echo "========================================="
echo "  历史人物对话系统 - 文件导出"
echo "========================================="
echo ""

PROJECT_ROOT="/workspace/projects"

# 创建导出清单
cat > "$PROJECT_ROOT/EXPORT_MANIFEST.txt" << 'MANIFEST'
=======================================
历史人物对话系统 - 文件清单
=======================================

请将以下文件复制到你的本地电脑：

【配置文件】
1. config/agent_llm_config.json
2. assets/historical_figures.json

【后端核心】
1. src/app.py
2. src/agents/agent.py
3. src/tools/historical_figure_tool.py
4. src/storage/memory/memory_saver.py

【API 接口】
1. src/api/__init__.py
2. src/api/routes/chat.py
3. src/api/routes/websocket.py
4. src/api/routes/voice.py
5. src/api/routes/model3d.py

【前端界面】
1. frontend/index.html

【依赖文件】
1. requirements.txt

【部署文档】
1. LOCAL_SETUP.md - 本地部署指南
2. README.md - 项目说明
MANIFEST

echo "文件清单已创建: EXPORT_MANIFEST.txt"
echo ""

# 验证所有文件是否存在
echo "正在检查文件..."
echo ""

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 (缺失)"
    fi
}

# 检查配置文件
check_file "$PROJECT_ROOT/config/agent_llm_config.json"
check_file "$PROJECT_ROOT/assets/historical_figures.json"

# 检查后端文件
check_file "$PROJECT_ROOT/src/app.py"
check_file "$PROJECT_ROOT/src/agents/agent.py"
check_file "$PROJECT_ROOT/src/tools/historical_figure_tool.py"
check_file "$PROJECT_ROOT/src/storage/memory/memory_saver.py"

# 检查 API 文件
check_file "$PROJECT_ROOT/src/api/__init__.py"
check_file "$PROJECT_ROOT/src/api/routes/chat.py"
check_file "$PROJECT_ROOT/src/api/routes/websocket.py"
check_file "$PROJECT_ROOT/src/api/routes/voice.py"
check_file "$PROJECT_ROOT/src/api/routes/model3d.py"

# 检查前端文件
check_file "$PROJECT_ROOT/frontend/index.html"

# 检查依赖文件
check_file "$PROJECT_ROOT/requirements.txt"

echo ""
echo "========================================="
echo "检查完成！"
echo "========================================="
echo ""
echo "下一步："
echo "1. 查看 LOCAL_SETUP.md 了解部署步骤"
echo "2. 根据文件清单复制所有文件到本地"
echo "3. 按照本地部署指南启动服务"
echo ""
