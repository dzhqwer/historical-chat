from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="历史人物对话 API",
    description="沉浸式历史人物对话系统后端接口",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from src.api.routes import chat, figures, websocket, voice, model3d

# 注册路由
app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])
app.include_router(figures.router, prefix="/api/figures", tags=["历史人物"])
app.include_router(websocket.router, prefix="/api", tags=["WebSocket"])
app.include_router(voice.router, prefix="/api/voice", tags=["语音"])
app.include_router(model3d.router, prefix="/api/3d", tags=["3D模型"])


@app.get("/")
async def root():
    return {
        "message": "历史人物对话 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
