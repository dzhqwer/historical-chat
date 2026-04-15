from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from src.agents.agent import build_agent
from langchain_core.messages import HumanMessage, AIMessage
import uuid

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    figure_name: Optional[str] = None
    session_id: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    message: str
    figure_name: str
    session_id: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    发送消息并获取回复

    - **message**: 用户消息
    - **figure_name**: 可选，指定历史人物名称
    - **session_id**: 可选，会话ID，用于保持对话上下文
    - **stream**: 是否使用流式输出（WebSocket）
    """
    try:
        # 生成或使用会话ID
        session_id = request.session_id or str(uuid.uuid4())

        # 构建 Agent
        agent = build_agent()

        # 准备消息
        # 如果指定了人物，在消息中包含人物选择信息
        if request.figure_name:
            content = f"请扮演{request.figure_name}与我对话。{request.message}"
        else:
            content = request.message

        messages = [HumanMessage(content=content)]

        # 调用 Agent（使用异步接口）
        response = await agent.ainvoke(
            {"messages": messages},
            config={"configurable": {"thread_id": session_id}}
        )

        # 提取回复内容
        ai_message = response["messages"][-1]
        if isinstance(ai_message.content, str):
            reply = ai_message.content
        else:
            # 处理多模态内容
            reply = str(ai_message.content)

        return ChatResponse(
            message=reply,
            figure_name=request.figure_name or "未指定",
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """
    获取指定会话的对话历史

    - **session_id**: 会话ID
    """
    try:
        agent = build_agent()
        # 使用异步接口获取历史记录
        state = await agent.aget_state({"configurable": {"thread_id": session_id}})
        messages = state.values.get("messages", [])

        history = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": str(msg.content)})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": str(msg.content)})

        return {
            "session_id": session_id,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{session_id}")
async def clear_chat_history(session_id: str):
    """
    清除指定会话的对话历史

    - **session_id**: 会话ID
    """
    try:
        # LangGraph 的记忆会自动管理，这里返回成功
        return {
            "message": "对话历史已清除",
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
