from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
import json
from src.agents.agent import build_agent
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.base import BaseCheckpointSaver
import asyncio

router = APIRouter()


class ConnectionManager:
    """WebSocket 连接管理器"""
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    session_id: Optional[str] = Query(None)
):
    """
    WebSocket 实时流式对话接口

    连接参数:
    - **session_id**: 可选，会话ID。如果不提供，将自动生成

    消息格式:
    ```json
    {
        "type": "message",
        "content": "用户消息",
        "figure_name": "可选，历史人物名称"
    }
    ```

    服务器响应格式:
    ```json
    {
        "type": "chunk",
        "content": "流式输出内容片段",
        "figure_name": "历史人物名称",
        "session_id": "会话ID"
    }
    ```
    """
    if not session_id:
        import uuid
        session_id = str(uuid.uuid4())

    await manager.connect(websocket, session_id)

    try:
        # 构建Agent
        agent = build_agent()

        # 发送连接成功消息
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "message": "WebSocket 连接成功"
        })

        # 监听消息
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            msg_type = message_data.get("type", "message")

            if msg_type == "message":
                content = message_data.get("content", "")
                figure_name = message_data.get("figure_name", None)

                if not content:
                    await websocket.send_json({
                        "type": "error",
                        "message": "消息内容不能为空"
                    })
                    continue

                try:
                    # 准备消息
                    # 如果指定了人物，在消息中包含人物选择信息
                    if figure_name:
                        content = f"请扮演{figure_name}与我对话。{content}"

                    # 准备消息
                    messages = [HumanMessage(content=content)]

                    # 先获取完整响应
                    response = await agent.ainvoke(
                        {"messages": messages},
                        config={"configurable": {"thread_id": session_id}}
                    )

                    # 提取回复内容
                    ai_message = response["messages"][-1]
                    if isinstance(ai_message.content, str):
                        full_reply = ai_message.content
                    else:
                        full_reply = str(ai_message.content)

                    # 模拟流式输出：逐字发送
                    for char in full_reply:
                        await websocket.send_json({
                            "type": "chunk",
                            "content": char,
                            "figure_name": figure_name or "未指定",
                            "session_id": session_id
                        })
                        # 添加延迟，模拟打字效果
                        await asyncio.sleep(0.02)

                    # 发送完成消息
                    await websocket.send_json({
                        "type": "done",
                        "session_id": session_id
                    })

                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"处理消息时出错: {str(e)}"
                    })

            elif msg_type == "ping":
                # 心跳检测
                await websocket.send_json({
                    "type": "pong"
                })

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        print(f"Session {session_id} disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(session_id)
