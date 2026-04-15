# 3D 模型 API 文档

## 概述

3D 模型模块提供历史人物图像生成、3D 模型配置管理和口型同步功能，为沉浸式对话体验提供视觉支持。

---

## 图像生成

### 生成历史人物图像

**接口**: `POST /api/3d/generate-image`

**请求参数**:
```json
{
  "figure_name": "李白",
  "style": "realistic",
  "size": "2K",
  "pose": "portrait",
  "expression": "thoughtful"
}
```

**参数说明**:
- `figure_name` (string, required): 历史人物名称
- `style` (string, optional): 图像风格
  - `realistic`: 写实风格（默认）
  - `anime`: 动漫风格
  - `painting`: 油画风格
  - `3d_render`: 3D 渲染风格
- `size` (string, optional): 图像大小
  - `2K`: 2K 分辨率（默认）
  - `4K`: 4K 分辨率
- `pose` (string, optional): 姿势
  - `portrait`: 肖像特写（默认）
  - `half_body`: 半身像
  - `full_body`: 全身像
- `expression` (string, optional): 表情
  - `neutral`: 中性表情（默认）
  - `smile`: 微笑
  - `thoughtful`: 沉思
  - `serious`: 严肃

**响应示例**:
```json
{
  "figure_name": "李白",
  "image_url": "https://coze-coding-project.tos.coze.site/...",
  "style": "realistic",
  "size": "2K",
  "prompt": "A photorealistic portrait of historical figure 李白..."
}
```

---

## 3D 模型配置

### 获取所有 3D 模型配置

**接口**: `GET /api/3d/models`

**响应示例**:
```json
{
  "models": {
    "李白": {
      "image_url": "https://...",
      "style": "realistic",
      "size": "2K",
      "pose": "portrait",
      "expression": "thoughtful"
    },
    "爱因斯坦": {
      "image_url": null,
      "style": "realistic",
      "size": "2K",
      "pose": "portrait",
      "expression": "neutral"
    }
  },
  "count": 8
}
```

### 获取指定人物的 3D 模型配置

**接口**: `GET /api/3d/models/{figure_name}`

**参数**:
- `figure_name`: 历史人物名称

**响应示例**:
```json
{
  "image_url": "https://...",
  "style": "realistic",
  "size": "2K",
  "pose": "portrait",
  "expression": "thoughtful"
}
```

---

## 口型同步

### 生成口型同步数据

**接口**: `POST /api/3d/lip-sync`

**请求参数**:
```json
{
  "text": "床前明月光，疑是地上霜。",
  "figure_name": "李白"
}
```

**参数说明**:
- `text` (string, required): 要合成口型动画的文本
- `figure_name` (string, optional): 历史人物名称（可选，用于未来扩展）

**响应示例**:
```json
{
  "text": "床前明月光，疑是地上霜。",
  "visemes": [
    {
      "index": 0,
      "char": "床",
      "viseme": "ai",
      "time": 0.0,
      "duration": 0.15
    },
    {
      "index": 1,
      "char": "前",
      "viseme": "ai",
      "time": 0.15,
      "duration": 0.15
    },
    {
      "index": 6,
      "char": "，",
      "viseme": "sil",
      "time": 0.75,
      "duration": 0.3
    }
  ],
  "duration": 2.1
}
```

**Viseme 数据说明**:
- `index`: 音素索引
- `char`: 对应的字符
- `viseme`: 音素 ID（见下方音素列表）
- `time`: 音素开始时间（秒）
- `duration`: 音素持续时间（秒）

### 获取音素列表

**接口**: `GET /api/3d/visemes`

**响应示例**:
```json
{
  "visemes": [
    {
      "id": "sil",
      "name": "静默",
      "description": "闭嘴状态"
    },
    {
      "id": "ai",
      "name": "张大嘴",
      "description": "嘴部张开，如 'a'"
    },
    {
      "id": "e",
      "name": "咧嘴",
      "description": "嘴角向两边拉开，如 'e'"
    },
    ...
  ],
  "count": 21
}
```

**完整音素列表**:

| ID | 名称 | 描述 | 示例 |
|----|------|------|------|
| sil | 静默 | 闭嘴状态 | 标点、停顿 |
| ai | 张大嘴 | 嘴部张开 | a, 阿 |
| e | 咧嘴 | 嘴角向两边拉开 | e, 额 |
| i | 咧嘴微笑 | 嘴角向上拉 | i, 衣 |
| o | 圆嘴 | 嘴唇呈圆形 | o, 哦 |
| u | 嘟嘴 | 嘴唇前突 | u, 乌 |
| p | 双唇紧闭 | 双唇紧闭准备爆破 | p, b |
| m | 闭嘴鼻音 | 双唇紧闭发鼻音 | m |
| f | 上牙咬下唇 | 上牙轻咬下唇 | f, v |
| t | 舌尖抵齿 | 舌尖抵住上齿 | t, d |
| n | 舌尖齿龈 | 舌尖抵齿龈发鼻音 | n |
| l | 舌尖卷起 | 舌尖卷起 | l |
| k | 舌根抬起 | 舌根抬起 | k, g |
| h | 张口呼吸 | 嘴部微张，气流通过 | h |
| ch | 翘舌音 | 舌尖卷起 | ch, sh, zh, j, q, x |
| sh | 舌音 | 舌头靠近硬腭 | sh, r |
| r | 卷舌 | 舌头上卷 | r |
| s | 齿音 | 舌近上齿 | s, c, z |
| y | 半元音 | 舌前抬高 | y |
| w | 圆唇 | 双唇收圆 | w |

---

## 使用示例

### Python 示例

#### 生成历史人物图像
```python
import requests

data = {
    "figure_name": "李白",
    "style": "realistic",
    "size": "2K",
    "pose": "portrait",
    "expression": "thoughtful"
}

response = requests.post(
    "http://localhost:8000/api/3d/generate-image",
    json=data
)

result = response.json()
image_url = result['image_url']

# 下载图像
img_data = requests.get(image_url).content
with open("libai_portrait.png", "wb") as f:
    f.write(img_data)
```

#### 生成口型同步数据
```python
import requests

data = {
    "text": "床前明月光，疑是地上霜。",
    "figure_name": "李白"
}

response = requests.post(
    "http://localhost:8000/api/3d/lip-sync",
    json=data
)

result = response.json()
visemes = result['visemes']
duration = result['duration']

# 遍历音素序列
for v in visemes:
    print(f"{v['time']:.2f}s: {v['char']} -> {v['viseme']}")
```

#### 完整工作流程
```python
import requests

# 1. 发送对话消息
chat_data = {
    "message": "请介绍一下你自己",
    "figure_name": "李白"
}

chat_response = requests.post(
    "http://localhost:8000/api/chat/",
    json=chat_data
)
reply_text = chat_response.json()["message"]

# 2. 生成口型同步数据
lip_sync_data = {
    "text": reply_text,
    "figure_name": "李白"
}

lip_sync_response = requests.post(
    "http://localhost:8000/api/3d/lip-sync",
    json=lip_sync_data
)
visemes = lip_sync_response.json()["visemes"]

# 3. 生成语音
tts_data = {
    "text": reply_text,
    "figure_name": "李白"
}

tts_response = requests.post(
    "http://localhost:8000/api/voice/tts",
    json=tts_data
)
audio_url = tts_response.json()["audio_url"]

# 4. 在前端使用
# - 使用 visemes 控制 3D 模型的口型动画
# - 播放 audio_url 的音频
# - 同步口型动画和音频播放
```

---

## 前端集成指南

### Three.js 3D 模型展示

```javascript
import * as THREE from 'three';

// 创建场景
const scene = new THREE.Scene();

// 创建相机
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// 创建渲染器
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 加载人物图像作为纹理
const textureLoader = new THREE.TextureLoader();
const texture = textureLoader.load('https://...libai_portrait.png');

// 创建平面几何体
const geometry = new THREE.PlaneGeometry(4, 5);
const material = new THREE.MeshBasicMaterial({
    map: texture,
    transparent: true
});

// 创建 3D 模型
const character = new THREE.Mesh(geometry, material);
scene.add(character);

// 添加口型动画
function updateLipSync(visemes, currentTime) {
    const activeViseme = visemes.find(v =>
        currentTime >= v.time && currentTime < v.time + v.duration
    );

    if (activeViseme) {
        // 根据音素调整模型口型
        applyVisemeToModel(activeViseme.viseme);
    }
}

// 渲染循环
function animate() {
    requestAnimationFrame(animate);

    const currentTime = audioElement.currentTime;
    updateLipSync(visemes, currentTime);

    renderer.render(scene, camera);
}

animate();
```

---

## 测试

运行 3D 功能测试脚本：
```bash
python scripts/test_3d.py
```

测试内容包括：
1. 获取音素列表
2. 口型同步数据生成（短文本）
3. 长文本口型同步
4. 获取 3D 模型配置
5. 生成历史人物图像（可选，耗时较长）
6. 完整工作流程测试

---

## 注意事项

1. **图像生成时间**:
   - 图像生成需要 10-30 秒
   - 建议在后台预生成常用人物的图像

2. **图像 URL 有效期**:
   - 生成的图像 URL 有效期为 24 小时
   - 建议及时下载并保存到本地或对象存储

3. **口型同步精度**:
   - 当前实现基于字符级别的简单映射
   - 汉字使用通用音素，建议使用 pinyin 库进行精确转换
   - 可集成专业的口型同步服务提升精度

4. **性能优化**:
   - 图像生成建议使用异步任务队列
   - 音素数据可以缓存
   - 3D 渲染建议使用 GPU 加速

5. **前端集成**:
   - 口型动画需要与音频播放精确同步
   - 建议使用 Web Audio API 进行音频分析
   - 3D 模型可以结合表情动画增强表现力
