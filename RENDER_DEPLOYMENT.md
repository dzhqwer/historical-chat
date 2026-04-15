# 🚀 部署到 Render.com - 完整指南

## 📋 部署方案

### 架构说明

为了免费部署，我们采用：

- **后端**：Render.com（免费服务）
- **前端**：GitHub Pages（完全免费）

这样可以避免 Render 免费版只能部署一个服务的限制。

---

## 🎯 第 1 步：准备 GitHub 仓库

### 1.1 创建 GitHub 账号（如果没有）

访问：https://github.com/signup

### 1.2 创建新仓库

1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 仓库名称：`historical-chat`
4. 选择 "Public"
5. 点击 "Create repository"

---

## 🎯 第 2 步：上传代码到 GitHub

### 2.1 在你的本地电脑上初始化 Git

在 `historical-chat` 文件夹中打开命令行：

```batch
cd historical-chat
git init
git add .
git commit -m "Initial commit"
```

### 2.2 连接到 GitHub

```batch
git branch -M main
git remote add origin https://github.com/你的用户名/historical-chat.git
git push -u origin main
```

**替换 `你的用户名` 为你的 GitHub 用户名**

---

## 🎯 第 3 步：部署前端到 GitHub Pages

### 3.1 进入仓库设置

1. 访问你的 GitHub 仓库
2. 点击 "Settings"
3. 在左侧菜单找到 "Pages"

### 3.2 配置 Pages

1. Source 选择 "Deploy from a branch"
2. Branch 选择 `main`，目录选择 `/ (root)`
3. 点击 "Save"

### 3.3 创建 frontend 子文件夹的链接

由于 GitHub Pages 默认从根目录部署，我们需要创建一个符号链接：

**在 `historical-chat` 文件夹中**：

```batch
cd frontend
mkdir .well-known
cd .well-known
echo "{\"web\":{\"directory\":\"/\"}}" > build-info.json
cd ..
```

或者直接复制 `frontend/index.html` 到根目录：

```batch
copy frontend\index.html index.html
```

### 3.4 获取前端 URL

等待 1-2 分钟后，访问：
```
https://你的用户名.github.io/historical-chat/
```

**记下这个地址**，后面会用到。

---

## 🎯 第 4 步：修改前端配置

打开 `frontend/index.html`，找到并修改 API 地址：

```javascript
const API_BASE = 'https://historical-chat-api.onrender.com';
```

**修改为你的 Render 后端地址**（部署后会得到）

---

## 🎯 第 5 步：部署后端到 Render

### 5.1 注册 Render 账号

1. 访问：https://render.com/
2. 点击 "Sign Up"
3. 使用 GitHub 账号登录（推荐）

### 5.2 创建新的 Web Service

1. 登录 Render Dashboard
2. 点击 "New +" → "Web Service"
3. 选择 "Build and deploy from a Git repository"
4. 选择你的 GitHub 仓库 `historical-chat`
5. 点击 "Connect"

### 5.3 配置服务

填写以下信息：

- **Name**: `historical-chat-api`
- **Region**: `Oregon` (免费版)
- **Branch**: `main`
- **Runtime**: `Python`
- **Build Command**: `pip install -r requirements-render.txt`
- **Start Command**: `uvicorn src.app:app --host 0.0.0.0 --port $PORT`

### 5.4 设置环境变量

在 "Environment" 部分，点击 "Add Environment Variable"：

```
Key: COZE_WORKLOAD_IDENTITY_API_KEY
Value: 你的 Coze API 密钥
```

```
Key: COZE_INTEGRATION_MODEL_BASE_URL
Value: https://api.coze.cn/open_api/v2
```

### 5.5 部署

点击 "Create Web Service"

Render 会自动：
1. 检测到 Python 环境
2. 安装依赖
3. 启动服务

---

## 🎯 第 6 步：获取后端 URL

1. 在 Render Dashboard 找到你的服务
2. 服务名称旁边有一个 URL，例如：
   ```
   https://historical-chat-api.onrender.com
   ```

**记下这个地址**。

---

## 🎯 第 7 步：更新前端配置

回到你的 GitHub 仓库，编辑 `frontend/index.html`：

```javascript
const API_BASE = 'https://historical-chat-api.onrender.com';
```

替换为你的实际后端地址。

---

## 🎯 第 8 步：重新部署前端

推送更新到 GitHub：

```batch
git add frontend/index.html
git commit -m "Update API endpoint"
git push
```

GitHub Pages 会自动重新部署。

---

## ✅ 部署完成！

### 访问你的应用

打开浏览器，访问你的 GitHub Pages 地址：
```
https://你的用户名.github.io/historical-chat/
```

### 测试

1. 选择一个历史人物（如李白）
2. 发送消息："你好"
3. 查看是否收到回复

---

## 🔧 故障排查

### 问题 1：后端部署失败

**检查**：
1. Build Command 是否正确：`pip install -r requirements-render.txt`
2. Start Command 是否正确：`uvicorn src.app:app --host 0.0.0.0 --port $PORT`
3. 环境变量是否正确设置

### 问题 2：前端无法连接后端

**检查**：
1. API 地址是否正确
2. 后端是否成功启动
3. CORS 是否正确配置（已在 `src/app.py` 中配置）

### 问题 3：服务自动休眠

**原因**：Render 免费版 15 分钟无请求会自动休眠

**解决**：
- 首次访问可能需要等待 30-60 秒唤醒
- 可以使用第三方工具定期 ping 保持唤醒

---

## 💰 免费额度

### Render 免费版
- ✅ 512MB RAM
- ✅ 512MB 磁盘
- ✅ 750 小时/月
- ⚠️ 15 分钟无请求自动休眠

### GitHub Pages
- ✅ 完全免费
- ✅ 无限制带宽
- ✅ 自动 HTTPS
- ✅ 全球 CDN

---

## 📚 更多信息

- Render 文档：https://render.com/docs
- GitHub Pages 文档：https://docs.github.com/en/pages

---

## 🎉 完成！

现在你拥有了一个完全免费的历史人物对话系统！

祝使用愉快！🚀
