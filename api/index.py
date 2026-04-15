import subprocess
import sys

# 在运行时安装依赖（Vercel 限制）
def install_dependencies():
    """动态安装必需的依赖"""
    required_packages = [
        "fastapi",
        "uvicorn[standard]",
        "langchain",
        "langchain-openai",
        "langgraph",
        "openai",
        "pydantic",
        "python-dotenv",
        "duckduckgo-search",
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", package])

# 安装依赖
install_dependencies()

# 现在导入应用
from src.app import app

# Vercel Serverless Function 入口
handler = app
