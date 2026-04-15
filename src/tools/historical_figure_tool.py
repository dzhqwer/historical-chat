import asyncio
from duckduckgo_search import DDGS
from langchain.tools import tool


@tool
def search_historical_info(query: str) -> str:
    """
    搜索历史人物的相关信息

    Args:
        query: 搜索查询词

    Returns:
        搜索结果摘要
    """
    try:
        # 使用 DuckDuckGo 搜索
        results = DDGS().text(query, max_results=5)

        if not results:
            return "未找到相关信息"

        # 格式化结果
        summary = f"关于 {query} 的搜索结果：\n\n"
        for i, result in enumerate(results[:3], 1):
            summary += f"{i}. {result.get('title', '')}\n"
            summary += f"   {result.get('body', '')[:100]}...\n"
            summary += f"   来源: {result.get('href', '')}\n\n"

        return summary

    except Exception as e:
        return f"搜索失败: {str(e)}"


@tool
def get_historical_context(figure_name: str) -> str:
    """
    获取历史人物的时代背景信息

    Args:
        figure_name: 历史人物名称

    Returns:
        时代背景描述
    """
    # 使用搜索获取背景信息
    return search_historical_info(f"{figure_name} 时代背景 生平事迹")