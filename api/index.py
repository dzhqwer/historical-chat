import json
from typing import Dict, Any

# 内置的历史人物数据（不依赖文件读取）
FIGURES_DATA = {
    "figures": [
        {
            "id": 1,
            "name": "李白",
            "era": "唐代",
            "description": "唐代著名诗人，字太白，号青莲居士。创作了大量脍炙人口的诗篇。",
            "avatar": "👨‍🎤"
        },
        {
            "id": 2,
            "name": "孔子",
            "era": "春秋",
            "description": "儒家学派创始人，伟大的思想家、教育家，被尊为'至圣先师'。",
            "avatar": "👴"
        },
        {
            "id": 3,
            "name": "爱因斯坦",
            "era": "现代",
            "description": "理论物理学家，相对论创立者，诺贝尔物理学奖获得者。",
            "avatar": "👨‍🔬"
        },
        {
            "id": 4,
            "name": "牛顿",
            "era": "近代",
            "description": "物理学家、数学家，经典力学体系的创立者。",
            "avatar": "👨‍🔬"
        },
        {
            "id": 5,
            "name": "莎士比亚",
            "era": "文艺复兴",
            "description": "英国剧作家、诗人，创作了《哈姆雷特》、《罗密欧与朱丽叶》等经典作品。",
            "avatar": "🎭"
        }
    ]
}

# 内置的配置数据（不依赖文件读取）
CONFIG_DATA = {
    "config": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 1000,
        "timeout": 600,
        "thinking": "disabled"
    },
    "sp": "你是历史人物对话助手，请用符合历史人物身份、口吻和时代背景的语言风格与用户进行对话。"
}

# Vercel Serverless Function 入口
def handler(request):
    """处理所有 API 请求"""
    try:
        # 获取请求路径
        path = request.get('path', '').lstrip('/')
        
        # 处理不同的路由
        if path == '' or path == 'api':
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "Historical Chat API is running!",
                    "version": "1.0.0",
                    "endpoints": {
                        "/api/figures": "获取历史人物列表",
                        "/api/chat": "对话接口",
                        "/api/config": "获取配置信息"
                    }
                }, ensure_ascii=False)
            }
        
        elif path == 'figures':
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(FIGURES_DATA, ensure_ascii=False)
            }
        
        elif path == 'config':
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(CONFIG_DATA, ensure_ascii=False)
            }
        
        elif path == 'chat':
            # 简单的对话接口（返回模拟响应）
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "对话功能需要配置真实的 LLM API，当前返回模拟响应",
                    "response": "你好！我是历史人物对话助手。请选择一个历史人物开始对话。"
                }, ensure_ascii=False)
            }
        
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "error": "Not Found",
                    "message": f"路径 /{path} 不存在"
                })
            }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Internal Server Error",
                "message": str(e)
            })
        }

# Lambda 函数入口（Vercel 使用）
def lambda_handler(event, context):
    """AWS Lambda 兼容入口"""
    return handler(event)
