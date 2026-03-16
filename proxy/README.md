# Tavily API Proxy

把多个 Tavily API Key 做成一个统一代理池，对外暴露固定接口和自定义 Token，并提供一个可视化控制台。

这版 `proxy` 已经不是简单的“本地估算额度”了，后台会通过 Tavily 官方 `GET /usage` 接口同步每个 Key 的真实已用额度、剩余额度和账户计划信息。

## Docker Image

Docker Hub 镜像地址：

```text
docker.io/skernelx/tavily-proxy:latest
```

也可以直接这样拉取：

```bash
docker pull skernelx/tavily-proxy:latest
```

## 功能

- 多个 Tavily Key 轮询代理
- 自定义访问 Token
- Token 级限流
- Web 控制台
- 批量导入 Key
- 真实同步 Tavily 官方额度
- 同时保留代理侧成功 / 失败 / 延迟统计
- 与 Tavily 官方 API 保持兼容

## 推荐部署方式

### 1. 直接用 Docker Hub 镜像启动

```bash
mkdir -p tavily-proxy-data

docker run -d \
  --name tavily-proxy \
  --restart unless-stopped \
  -p 9874:9874 \
  -e ADMIN_PASSWORD=your-admin-password \
  -v $(pwd)/tavily-proxy-data:/app/data \
  skernelx/tavily-proxy:latest
```

启动后访问：

```text
http://localhost:9874
```

### 2. 使用 docker compose

你也可以直接用仓库里的 compose：

```bash
cd proxy
docker compose up -d
```

默认 compose 会：

- 暴露端口 `9874`
- 把数据库挂载到 `./data`
- 用 `ADMIN_PASSWORD` 作为控制台密码

### 3. 本地源码运行

```bash
cd proxy
pip install -r requirements.txt
ADMIN_PASSWORD=your-admin-password uvicorn server:app --host 0.0.0.0 --port 9874
```

## 更新方式

如果你已经在服务器上跑了旧容器，后续更新推荐直接：

```bash
docker pull skernelx/tavily-proxy:latest

docker rm -f tavily-proxy

docker run -d \
  --name tavily-proxy \
  --restart unless-stopped \
  -p 9874:9874 \
  -e ADMIN_PASSWORD=your-admin-password \
  -v /your/data/path:/app/data \
  skernelx/tavily-proxy:latest
```

只要你保留原来的数据卷目录，Key、Token 和控制台密码都会继续保留。

## 控制台里现在能看到什么

当前控制台会分成两套统计：

### 1. Tavily 官方真实额度

来自官方 `GET /usage`：

- 单个 Key 的真实已用
- 单个 Key 的真实剩余
- 账户计划名
- 账户总额度
- 账户已用 / 剩余

如果某个 Key 本身没有独立 `limit`，后台会自动回退到账户计划额度，而不是继续自己瞎算。

### 2. 代理自身统计

来自本地 `usage_logs`：

- 成功次数
- 失败次数
- 今日用量
- 本月代理用量
- Token 级配额消耗

## 使用流程

1. 启动 proxy
2. 打开控制台
3. 输入管理密码登录
4. 导入 Tavily Key
5. 创建一个 Token
6. 把这个 Token 给你的客户端使用
7. 控制台里查看真实额度和代理统计

## API 调用方式

代理保持 Tavily 官方接口风格，常用端点有：

- `POST /api/search`
- `POST /api/extract`

认证方式支持两种：

- `Authorization: Bearer YOUR_TOKEN`
- body 里传 `api_key`

### Search 示例

```bash
curl -X POST http://localhost:9874/api/search \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "hello world", "max_results": 1}'
```

### Extract 示例

```bash
curl -X POST http://localhost:9874/api/extract \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com"]}'
```

### 也可以在 body 里传 token

```bash
curl -X POST http://localhost:9874/api/search \
  -H "Content-Type: application/json" \
  -d '{"api_key": "YOUR_TOKEN", "query": "hello world"}'
```

## 管理 API

所有管理 API 需要：

- `X-Admin-Password: your-admin-password`

或者：

- `Authorization: Bearer your-admin-password`

### 常用管理端点

- `GET /api/stats`
  返回概览、Token 统计、真实额度汇总

- `GET /api/keys`
  返回 Key 列表和脱敏信息

- `POST /api/keys`
  添加单个 Key 或批量导入

- `PUT /api/keys/{id}/toggle`
  启用 / 禁用某个 Key

- `DELETE /api/keys/{id}`
  删除 Key

- `GET /api/tokens`
  获取 Token 列表

- `POST /api/tokens`
  创建 Token

- `DELETE /api/tokens/{id}`
  删除 Token

- `POST /api/usage/sync`
  手动同步 Tavily 官方真实额度

- `PUT /api/password`
  修改控制台密码

## 配置项

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `ADMIN_PASSWORD` | `admin` | 控制台登录密码 |
| `USAGE_SYNC_TTL_SECONDS` | `300` | 真实额度缓存秒数 |
| `USAGE_SYNC_CONCURRENCY` | `4` | 并发同步 `/usage` 的最大 Key 数 |

## 数据持久化

SQLite 数据库默认保存在：

```text
/app/data/proxy.db
```

所以容器部署时一定要挂载数据卷。

例如：

```bash
-v /your/data/path:/app/data
```

## Token 配额

每个 Token 默认配额：

- 小时：100
- 每日：500
- 每月：5000

超过配额后会返回：

```text
429 Too Many Requests
```

## 适合什么场景

- 你有多个 Tavily Key，想做成一个统一入口
- 你不想在下游程序里到处散落真实 Tavily Key
- 你想知道每个 Key 的真实剩余额度，而不是自己估算
- 你想给不同项目分不同的代理 Token

## 注意事项

- 控制台里显示的“真实额度”依赖 Tavily 官方 `/usage`
- 如果某个 Key 被 Tavily 风控、失效或网络异常，同步状态里会显示错误
- 代理统计和官方真实额度不是一回事，两者都会保留
- 更新镜像时，只要不删数据卷，历史数据都会保留

## 推荐做法

如果你已经在用这个仓库的注册器主程序，最顺的链路其实是：

1. 用主程序批量注册并拿到 Key
2. 自动上传到你自己的 proxy
3. 由 proxy 统一对外提供 Token
4. 在控制台里看真实额度和代理消耗
