import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langgraph.checkpoint.memory import MemorySaver

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]

def build_agent(ctx=None):
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    # 获取 API 配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL", "https://api.coze.cn/open_api/v2")

    # 使用标准 OpenAI 客户端配置
    llm = ChatOpenAI(
        model=cfg['config'].get("model", "gpt-3.5-turbo"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
    )

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp", "你是一个有用的助手。"),
        tools=[],  # 工具通过其他方式实现
        checkpointer=MemorySaver(),
        state_schema=AgentState,
    )