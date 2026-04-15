from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.tools.historical_figure_tool import _load_figures_config, _get_all_figures_list

router = APIRouter()


@router.get("/")
async def get_figures():
    """
    获取所有历史人物列表
    """
    try:
        config = _load_figures_config()
        if not config:
            raise HTTPException(status_code=500, detail="无法加载配置文件")

        figures = config.get("figures", {})

        # 转换为前端友好的格式
        result = []
        for name, info in figures.items():
            result.append({
                "name": name,
                "title": info.get("title", ""),
                "era": info.get("era", ""),
                "style": info.get("style", ""),
                "famous_works": info.get("famous_works", [])
            })

        return {
            "figures": result,
            "count": len(result),
            "default": config.get("default_figure", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detail/{figure_name}")
async def get_figure_detail(figure_name: str):
    """
    获取指定历史人物的详细信息

    - **figure_name**: 历史人物名称
    """
    try:
        config = _load_figures_config()
        if not config:
            raise HTTPException(status_code=500, detail="无法加载配置文件")

        figures = config.get("figures", {})

        if figure_name not in figures:
            raise HTTPException(status_code=404, detail=f"未找到历史人物: {figure_name}")

        figure_info = figures[figure_name]

        return {
            "name": figure_info["name"],
            "title": figure_info.get("title", ""),
            "era": figure_info.get("era", ""),
            "style": figure_info.get("style", ""),
            "famous_works": figure_info.get("famous_works", []),
            "system_prompt": figure_info.get("system_prompt", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def get_figures_list():
    """
    获取历史人物列表（文本格式，用于 Agent 内部）
    """
    return _get_all_figures_list()
