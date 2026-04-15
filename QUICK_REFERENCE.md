# 🎯 快速参考

## Windows 常见问题

### ❌ 问题 1：双击脚本乱码

**解决方案**：
- 已在所有 `.bat` 脚本中添加 `chcp 65001` 自动切换 UTF-8 编码
- 如果仍乱码，尝试右键命令行窗口 → 属性 → 字体 → 选择"新宋体"或"SimHei"

### ❌ 问题 2：双击脚本窗口一闪而过

**解决方案**：
1. 按 `Win + R`，输入 `cmd`，按 Enter
2. 导航到项目目录：
   ```batch
   cd C:\你的项目路径\projects
   ```
3. 运行脚本：
   ```batch
   scripts\setup_windows.bat
   ```

或使用新创建的启动器：
```batch
scripts\run_check.bat
```

### ❌ 问题 3：端口被占用

**解决方案**：
- 查看占用端口的进程：
  ```batch
  netstat -ano | findstr ":8000"
  netstat -ano | findstr ":3000"
  ```
- 终止进程（替换 PID）：
  ```batch
  taskkill /PID 进程ID /F
  ```
- 或修改 `auto_start.bat` 中的端口号

### ❌ 问题 4：找不到 uvicorn 命令

**解决方案**：
```batch
# 重新同步依赖
uv sync

# 或使用 python -m 方式运行
python -m uvicorn src.app:app --port 8000
```

## 功能测试

### 1. 测试后端是否正常

```bash
curl http://localhost:8000/health
```

应返回：`{"status":"ok"}`

### 2. 测试前端是否正常

访问 http://localhost:3000，应看到聊天界面

### 3. 测试对话功能

选择一个历史人物（如"李白"），发送消息："你好"

### 4. 测试语音功能

点击麦克风图标，说话，应自动转换为文字

### 5. 测试 3D 模型

选择历史人物后，应自动显示 3D 形象

## 键盘快捷键

- **Ctrl+C**：终止服务
- **Ctrl+L**：清屏（Linux/Mac）
- **Ctrl+Break**：强制终止（Windows）

## 访问地址

| 服务 | 地址 | 说明 |
|-----|------|------|
| 前端界面 | http://localhost:3000 | 用户聊天界面 |
| 后端 API | http://localhost:8000 | API 服务 |
| API 文档 | http://localhost:8000/docs | Swagger 文档 |
| 健康检查 | http://localhost:8000/health | 服务状态检查 |

## 预设历史人物

- 🏮 **李白** - 唐代诗人，豪放浪漫
- 📜 **孔子** - 春秋思想家，儒家创始人
- 🔬 **爱因斯坦** - 物理学家，相对论
- 🎭 **莎士比亚** - 英国剧作家
- 💭 **苏格拉底** - 古希腊哲学家
- 🌊 **屈原** - 战国诗人
- 🔍 **牛顿** - 物理学家
- 🎨 **达芬奇** - 文艺复兴艺术家

## 目录结构

```
projects/
├── src/
│   ├── agents/         # Agent 核心逻辑
│   ├── tools/          # 工具函数
│   ├── api/            # API 路由
│   └── storage/        # 存储配置
├── frontend/           # 前端界面
├── config/             # 配置文件
├── assets/             # 资源文件
├── scripts/            # 启动脚本
│   ├── setup_windows.bat   # Windows 环境检查
│   └── auto_start.bat      # 自动启动服务
└── docs/               # 文档
```

## 开发模式

启用热重载（开发时使用）：

```bash
# 后端热重载
uvicorn src.app:app --port 8000 --reload

# 前端热重载（需要额外配置）
cd frontend
# 使用 live-server 或其他热重载工具
```

## 性能优化

1. **使用缓存**：Agent 已启用短期记忆缓存
2. **流式响应**：WebSocket 支持流式输出，提升响应速度
3. **CDN 加速**：前端使用 CDN 加载 React、Three.js 等库
4. **异步处理**：所有 API 使用 async/await

## 日志查看

- 后端日志：控制台输出
- 前端日志：浏览器开发者工具（F12）
- 错误日志：`/app/work/logs/bypass/app.log`（生产环境）
