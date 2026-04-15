# ⚡ Render 快速部署 - 10 分钟搞定

## 📋 准备清单

- [ ] GitHub 账号
- [ ] Render 账号
- [ ] Coze API 密钥

---

## 🚀 6 个步骤

### 1️⃣ 创建 GitHub 仓库（2分钟）

```
仓库名：historical-chat
公开：Public
```

### 2️⃣ 上传代码（3分钟）

```batch
cd historical-chat
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/historical-chat.git
git push -u origin main
```

### 3️⃣ 部署前端到 GitHub Pages（2分钟）

1. 仓库 → Settings → Pages
2. Source: Deploy from a branch
3. Branch: main / (root)
4. Save

**前端地址**：`https://你的用户名.github.io/historical-chat/`

### 4️⃣ 部署后端到 Render（3分钟）

1. Render → New Web Service
2. 连接 GitHub 仓库
3. 配置：
   - Runtime: Python
   - Build: `pip install -r requirements-render.txt`
   - Start: `uvicorn src.app:app --host 0.0.0.0 --port $PORT`
4. 环境变量：
   - `COZE_WORKLOAD_IDENTITY_API_KEY`: 你的密钥
   - `COZE_INTEGRATION_MODEL_BASE_URL`: `https://api.coze.cn/open_api/v2`

**后端地址**：`https://historical-chat-api.onrender.com`

### 5️⃣ 更新前端 API 地址（1分钟）

编辑 `frontend/index.html`：
```javascript
const API_BASE = 'https://historical-chat-api.onrender.com';
```

### 6️⃣ 推送更新（1分钟）

```batch
git add frontend/index.html
git commit -m "Update API"
git push
```

---

## ✅ 完成！

**访问**：`https://你的用户名.github.io/historical-chat/`

---

## 📝 快速命令

```bash
# 查看部署日志
Render Dashboard → Services → historical-chat-api → Logs

# 查看前端状态
GitHub 仓库 → Actions

# 重新部署
git push
```

---

## ⚠️ 注意

- Render 免费版：15分钟无请求自动休眠
- 首次访问：等待 30-60 秒唤醒
- 保持唤醒：使用 uptime robot 定期 ping

---

## 🆘 需要帮助？

查看详细指南：[RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)
