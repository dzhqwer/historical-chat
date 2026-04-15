# 语音功能 API 文档

## 概述

语音功能模块提供语音识别（ASR）和语音合成（TTS）能力，支持将语音转换为文本，以及将文本转换为语音。

---

## 语音识别（ASR）

### 1. 上传音频文件识别

**接口**: `POST /api/voice/asr`

**请求参数**:
- `audio_file` (file, required): 音频文件
  - 支持格式: WAV/MP3/OGG OPUS/M4A
  - 时长限制: ≤ 2小时
  - 文件大小: ≤ 100MB
- `uid` (string, optional): 用户唯一标识

**请求示例**:
```bash
curl -X POST "http://localhost:8000/api/voice/asr" \
  -F "audio_file=@audio.mp3" \
  -F "uid=user123"
```

**响应示例**:
```json
{
  "text": "识别出的文本内容",
  "duration": 3.5,
  "confidence": 0.98
}
```

### 2. 从 URL 识别

**接口**: `POST /api/voice/asr/url`

**请求参数**:
```json
{
  "audio_url": "https://example.com/audio.mp3",
  "uid": "user123"
}
```

**响应示例**:
```json
{
  "text": "识别出的文本内容",
  "duration": 3.5
}
```

---

## 语音合成（TTS）

### 1. 文字转语音

**接口**: `POST /api/voice/tts`

**请求参数**:
```json
{
  "text": "要合成的文字内容",
  "figure_name": "李白",
  "speaker": null,
  "audio_format": "mp3",
  "sample_rate": 24000,
  "speech_rate": 0,
  "loudness_rate": 0
}
```

**参数说明**:
- `text` (string, required): 要合成的文字
- `figure_name` (string, optional): 历史人物名称，自动选择对应音色
  - 支持的人物: 李白、爱因斯坦、孔子、秦始皇、莎士比亚、苏格拉底等
  - 优先级低于 `speaker`
- `speaker` (string, optional): 指定的音色 ID
  - 默认: `zh_female_xiaohe_uranus_bigtts`
  - 查看完整音色列表: `GET /api/voice/voices`
- `audio_format` (string, optional): 音频格式
  - 选项: `mp3`, `pcm`, `ogg_opus`
  - 默认: `mp3`
- `sample_rate` (integer, optional): 采样率
  - 范围: 8000-48000 Hz
  - 默认: 24000
- `speech_rate` (integer, optional): 语速调整
  - 范围: -50 到 100
  - 默认: 0（正常速度）
- `loudness_rate` (integer, optional): 音量调整
  - 范围: -50 到 100
  - 默认: 0（正常音量）

**响应示例**:
```json
{
  "audio_url": "https://coze-coding-project.tos.coze.site/...",
  "audio_size": 47085,
  "duration": 6.0,
  "speaker": "zh_female_xiaohe_uranus_bigtts"
}
```

---

## 音色管理

### 获取可用音色列表

**接口**: `GET /api/voice/voices`

**响应示例**:
```json
{
  "figure_voices": {
    "爱因斯坦": "zh_male_m191_uranus_bigtts",
    "牛顿": "zh_male_dayi_saturn_bigtts",
    "秦始皇": "zh_male_taocheng_uranus_bigtts",
    "苏格拉底": "zh_male_ruyayichen_saturn_bigtts",
    "李白": "zh_female_xiaohe_uranus_bigtts",
    "孔子": "zh_male_taocheng_uranus_bigtts",
    "莎士比亚": "zh_male_ruyayichen_saturn_bigtts",
    "default": "zh_female_xiaohe_uranus_bigtts"
  },
  "available_voices": [
    {
      "id": "zh_female_xiaohe_uranus_bigtts",
      "name": "小荷（通用女声）",
      "gender": "female",
      "style": "general"
    },
    {
      "id": "zh_male_m191_uranus_bigtts",
      "name": "云舟（通用男声）",
      "gender": "male",
      "style": "general"
    },
    ...
  ]
}
```

---

## 历史人物音色映射

系统为每个历史人物配置了相应的音色：

| 历史人物 | 音色 ID | 说明 |
|---------|---------|------|
| 爱因斯坦 | zh_male_m191_uranus_bigtts | 通用男声，智慧深沉 |
| 牛顿 | zh_male_dayi_saturn_bigtts | 视频配音男，专注严谨 |
| 秦始皇 | zh_male_taocheng_uranus_bigtts | 男声，果决雄豪 |
| 苏格拉底 | zh_male_ruyayichen_saturn_bigtts | 优雅男，循循善诱 |
| 毛泽东 | zh_male_dayi_saturn_bigtts | 视频配音男 |
| 李白 | zh_female_xiaohe_uranus_bigtts | 通用女声（可调整） |
| 孔子 | zh_male_taocheng_uranus_bigtts | 男声，温文尔雅 |
| 莎士比亚 | zh_male_ruyayichen_saturn_bigtts | 优雅男，诗意盎然 |

---

## 使用示例

### Python 示例

#### 语音识别
```python
import requests

# 上传音频文件
with open("audio.mp3", "rb") as f:
    files = {"audio_file": f}
    data = {"uid": "user123"}
    response = requests.post(
        "http://localhost:8000/api/voice/asr",
        files=files,
        data=data
    )

result = response.json()
print(f"识别结果: {result['text']}")
```

#### 语音合成
```python
import requests

# 使用历史人物音色
data = {
    "text": "床前明月光，疑是地上霜。",
    "figure_name": "李白"
}
response = requests.post(
    "http://localhost:8000/api/voice/tts",
    json=data
)

result = response.json()
print(f"音频 URL: {result['audio_url']}")
print(f"音频大小: {result['audio_size']} 字节")

# 下载音频
audio_data = requests.get(result['audio_url']).content
with open("output.mp3", "wb") as f:
    f.write(audio_data)
```

#### 对话 + 语音合成完整流程
```python
import requests

# 1. 发送对话消息
chat_data = {
    "message": "请介绍一下你自己",
    "figure_name": "孔子"
}
chat_response = requests.post(
    "http://localhost:8000/api/chat/",
    json=chat_data
)
reply_text = chat_response.json()["message"]

# 2. 将回复转换为语音
tts_data = {
    "text": reply_text,
    "figure_name": "孔子"
}
tts_response = requests.post(
    "http://localhost:8000/api/voice/tts",
    json=tts_data
)
audio_url = tts_response.json()["audio_url"]

# 3. 下载音频
audio_data = requests.get(audio_url).content
with open("confucius_reply.mp3", "wb") as f:
    f.write(audio_data)
```

---

## 测试

运行语音功能测试脚本：
```bash
python scripts/test_voice.py
```

测试内容包括：
1. 获取可用音色列表
2. TTS - 李白（使用人物音色）
3. TTS - 自定义音色（爱因斯坦）
4. 测试所有历史人物的语音合成
5. 对话 + 语音合成完整流程

---

## 注意事项

1. **音频格式限制**:
   - ASR: 支持 WAV/MP3/OGG OPUS/M4A
   - TTS: 支持 MP3/PCM/OGG OPUS

2. **文件大小限制**:
   - ASR: 音频时长 ≤ 2小时，文件大小 ≤ 100MB

3. **采样率范围**:
   - 8000-48000 Hz
   - 推荐值:
     - 8000-16000: 电话质量
     - 22050-24000: 标准质量（默认）
     - 32000-48000: 高质量

4. **语速和音量范围**:
   - 两者均为 -50 到 100
   - 负值: 减慢/降低
   - 0: 正常
   - 正值: 加快/提高

5. **音频 URL 有效期**:
   - 生成的音频 URL 有效期为 24 小时
   - 建议及时下载并保存到本地或对象存储

6. **音色选择优先级**:
   - `speaker` 参数 > `figure_name` 参数 > 默认音色
