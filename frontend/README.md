# 前端沉浸式对话界面

## 概述

这是历史人物沉浸式对话系统的前端界面，采用现代化设计，集成了所有后端功能。

## 功能特性

### ✨ 已实现功能

1. **3D 模型展示**
   - 基于 Three.js 的 3D 渲染
   - 动态加载历史人物图像
   - 平滑的浮动动画效果
   - 说话时的缩放动画

2. **对话系统**
   - 实时消息显示
   - 用户/AI 消息区分
   - 消息气泡动画效果
   - 自动滚动到最新消息

3. **语音功能**
   - 文字转语音（TTS）
   - 点击播放 AI 回复
   - 播放状态显示
   - 自动播放 AI 回复

4. **角色选择**
   - 角色选择器弹窗
   - 角色搜索功能
   - 角色信息展示
   - 快速切换角色

5. **用户界面**
   - 响应式设计
   - 深色主题
   - 现代化 UI 设计
   - 流畅的交互动画

## 快速开始

### 1. 启动后端服务

首先确保后端 API 服务正在运行：

```bash
cd /workspace/projects
./scripts/start_api.sh
```

服务将在 `http://localhost:8000` 启动。

### 2. 打开前端界面

使用浏览器打开前端文件：

```bash
# 方法 1: 直接用浏览器打开
open frontend/index.html

# 方法 2: 使用 Python 启动简单 HTTP 服务器
cd /workspace/projects/frontend
python -m http.server 3000

# 然后在浏览器访问
http://localhost:3000
```

### 3. 开始使用

1. 点击右上角的"切换人物"按钮
2. 选择你想对话的历史人物（如：李白、孔子、爱因斯坦等）
3. 在右侧输入框输入消息
4. 点击"发送"或按 Enter 键
5. AI 会以历史人物的身份回复
6. 可以点击"播放语音"按钮听 AI 的语音回复

## 界面布局

```
┌─────────────────────────────────────────────────────────┐
│  左侧：3D 模型展示区 (50%)    │  右侧：对话区 (50%)     │
│  ┌────────────────────────┐   │  ┌────────────────────┐  │
│  │                        │   │  │  消息列表         │  │
│  │   🎭 3D 模型           │   │  │  - 用户消息       │  │
│  │   历史人物形象         │   │  │  - AI 回复        │  │
│  │   动态浮动效果         │   │  │  - 语音播放按钮   │  │
│  │                        │   │  └────────────────────┘  │
│  │                        │   │  ┌────────────────────┐  │
│  └────────────────────────┘   │  │  输入框           │  │
│                              │  │  [输入消息...] [发送] │
│  [切换人物]                  │  └────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 核心组件

### Avatar3D（3D 模型组件）

负责渲染历史人物的 3D 模型展示。

**功能**：
- 加载并渲染人物图像
- 3D 空间中的平滑浮动动画
- 说话时的缩放动画
- 光晕效果

**使用**：
```jsx
<Avatar3D
    imageUrl="https://.../figure.png"
    figureName="李白"
    isSpeaking={true}
/>
```

### MessageBubble（消息气泡组件）

显示单条对话消息。

**功能**：
- 区分用户/AI 消息样式
- 语音播放按钮
- 播放状态切换
- 消息动画效果

**使用**：
```jsx
<MessageBubble
    message="你好，我是李白"
    isUser={false}
    figureName="李白"
/>
```

### FigureSelector（角色选择器）

历史人物选择弹窗。

**功能**：
- 角色列表展示
- 角色搜索
- 角色信息显示
- 快速切换

**使用**：
```jsx
<FigureSelector
    figures={figuresList}
    selectedFigure="李白"
    onSelect={handleSelect}
    onClose={handleClose}
/>
```

## API 集成

前端通过 `api` 对象与后端通信：

```javascript
// 获取历史人物列表
const figures = await api.getFigures();

// 发送消息
const response = await api.sendMessage(message, figureName, sessionId);

// 文字转语音
const ttsData = await api.textToSpeech(text, figureName);

// 获取口型同步数据
const lipSync = await api.getLipSync(text, figureName);

// 获取 3D 模型配置
const models = await api.get3DModels();
```

## 技术栈

- **React 18** - UI 框架
- **Three.js** - 3D 渲染引擎
- **Tailwind CSS** - 样式框架
- **Axios** - HTTP 客户端
- **Babel** - JSX 编译器

## 浏览器要求

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- 需要支持 WebGL
- 需要支持 ES6+

## 常见问题

### Q: 3D 模型不显示？

**A**: 检查以下几点：
1. 确保后端服务已启动
2. 确保人物图像已生成（调用 3D 图像生成 API）
3. 检查浏览器控制台是否有错误
4. 确认浏览器支持 WebGL

### Q: 语音播放失败？

**A**: 可能的原因：
1. 音频 URL 已过期（24 小时有效期）
2. 网络问题导致音频下载失败
3. 浏览器自动播放策略限制

### Q: 无法连接到后端？

**A**:
1. 确认后端服务在 `http://localhost:8000` 运行
2. 检查浏览器控制台的网络请求
3. 确认 CORS 配置正确
4. 检查防火墙设置

### Q: 消息发送后没有回复？

**A**:
1. 检查后端日志
2. 确认选择了历史人物
3. 检查网络连接
4. 确认 API 密钥配置正确

## 自定义和扩展

### 修改样式

可以在 `<style>` 标签中自定义样式：

```css
/* 修改消息气泡颜色 */
.message-bubble {
    background: #your-color;
}

/* 修改 3D 模型背景 */
.avatar-container {
    background: linear-gradient(...);
}
```

### 添加新功能

前端代码结构清晰，易于扩展：

1. **添加新的 API 方法**：
   ```javascript
   const api = {
       // 新增方法
       newMethod: async () => { ... }
   };
   ```

2. **创建新组件**：
   ```javascript
   function NewComponent({ props }) {
       return <div>...</div>;
   }
   ```

3. **集成新功能**：
   - 语音识别（ASR）
   - 表情识别
   - 手势识别
   - VR/AR 支持

## 性能优化

### 3D 渲染优化

- 使用贴图压缩
- 降低渲染分辨率
- 启用 LOD（细节层次）

### API 请求优化

- 请求缓存
- 并发请求
- 节流和防抖

### 动画优化

- 使用 CSS 动画代替 JS 动画
- 使用 requestAnimationFrame
- 减少重绘和回流

## 部署

### 静态部署

1. 将 `frontend/index.html` 放到 Web 服务器
2. 修改 API_BASE 为生产环境地址
3. 配置 HTTPS 和 CORS

### 使用 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend;
        index index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 未来计划

- [ ] 添加语音识别（ASR）功能
- [ ] 实现完整的口型同步动画
- [ ] 添加表情和手势
- [ ] 支持 VR/AR 模式
- [ ] 添加对话历史保存
- [ ] 支持多语言
- [ ] 添加对话分享功能
- [ ] 优化移动端体验

## 支持

如有问题，请查看：
- 后端 API 文档：`docs/API.md`
- 语音 API 文档：`docs/VOICE_API.md`
- 3D API 文档：`docs/3D_API.md`

---

**享受与历史人物的沉浸式对话体验！** 🎭✨
