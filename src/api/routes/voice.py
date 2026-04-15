import os
import uuid
import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from gtts import gTTS

router = APIRouter()


@router.post("/asr")
async def speech_to_text(audio: UploadFile = File(...)):
    """
    语音转文字（ASR）

    注意：当前版本由于 Railway 环境限制，暂不支持本地语音识别
    请使用文本输入，或稍后我们将集成云端 ASR API（Azure/Google）
    """
    return {
        "success": False,
        "error": "ASR 功能暂不可用，请使用文本输入。后续将支持云端语音识别 API。",
        "text": ""
    }


@router.post("/tts")
async def text_to_speech(text: str):
    """
    文字转语音（TTS）
    使用 gTTS（Google 免费语音）
    """
    output_file = f"/tmp/{uuid.uuid4()}.mp3"

    try:
        # 使用 gTTS 生成语音
        tts = gTTS(text=text, lang='zh-cn')
        tts.save(output_file)

        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))