# 阿里云函数计算部署指南

## 1. 准备工作

- 注册阿里云账号
- 开通函数计算服务
- 安装阿里云 CLI

## 2. 部署步骤

### 2.1 修改代码适配函数计算

将 FastAPI 应用改为函数计算格式：

```python
# index.py
from src.app import app
from mangum import Mangum

handler = Mangum(app)
```

### 2.2 创建函数

```bash
# 创建函数
fun create -t http -f historical-figures
```

### 2.3 上传代码

```bash
# 打包
zip -r function.zip . -x "*.pyc" "test_*"

# 上传
fun deploy
```

### 2.4 配置环境变量

在函数控制台配置：
- COZE_WORKSPACE_PATH
- COZE_WORKLOAD_IDENTITY_API_KEY
- COZE_INTEGRATION_MODEL_BASE_URL

### 2.5 配置前端

修改 frontend/index.html 中的 API_BASE 为函数计算域名：
```javascript
const API_BASE = 'https://your-function-id.aliyuncs.com';
```

## 3. 使用

访问函数计算提供的 HTTP 触发器 URL
```
https://your-function-id.aliyuncs.com
```

## 4. 优势

- 按量付费，成本低
- 自动扩缩容
- 免运维
- 高可用
```

