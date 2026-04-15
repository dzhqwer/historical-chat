from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

@router.get("/model/{figure_name}")
async def get_3d_model(figure_name: str) -> Dict[str, Any]:
    """获取历史人物的 3D 模型配置"""
    return {
        "type": "avatar",
        "name": figure_name,
        "url": "https://threejs.org/examples/models/gltf/Xbot.glb",
        "color": "#4A90E2",
        "animation": "idle"
    }

@router.post("/generate")
async def generate_custom_model(figure_data: Dict[str, Any]):
    """生成自定义 3D 模型配置"""
    return {
        "type": "custom",
        "name": figure_data.get("name", "Custom"),
        "url": "https://threejs.org/examples/models/gltf/Xbot.glb",
        "color": figure_data.get("color", "#4A90E2"),
        "animation": "idle"
    }