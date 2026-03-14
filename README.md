# Tavily Key Generator

自动批量注册 Tavily 账户并获取 API Key 的工具。

Auto batch register Tavily accounts and retrieve API Keys.

## 功能 / Features

- 基于 Playwright 的浏览器自动化注册
- Cloudflare Turnstile 验证码：免费浏览器模式 / CapSolver 付费 API
- 自动接收验证邮件并完成邮箱验证
- 可插拔邮箱后端：Cloudflare Email Worker / DuckMail
- 批量注册，自动保存 API Key

## 快速开始 / Quick Start

### 1. 克隆项目

```bash
git clone https://github.com/user/tavily-key-generator.git
cd tavily-key-generator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
playwright install firefox
```

### 3. 配置

```bash
cp config.example.py config.py
```

编辑 `config.py`，填写你的配置信息（见下方说明）。

### 4. 运行

```bash
python main.py
```

## 邮箱后端配置 / Email Backend

### Cloudflare Email Worker

需要自建 Cloudflare Email Worker（catch-all 模式接收邮件）。

```python
EMAIL_PROVIDER = "cloudflare"
EMAIL_DOMAIN = "example.com"        # 你的域名
EMAIL_PREFIX = "tavily"              # 邮箱前缀
EMAIL_API_URL = "https://mail.example.com"  # Worker URL
EMAIL_API_TOKEN = "your-token"       # API Token
```

### DuckMail

使用 DuckMail 临时邮箱服务，需要购买 API Key。

```python
EMAIL_PROVIDER = "duckmail"
DUCKMAIL_API_BASE = "https://api.duckmail.sbs"
DUCKMAIL_BEARER = "dk_xxx"           # DuckMail API Key
DUCKMAIL_DOMAIN = "duckmail.sbs"
```

## 验证码解决 / CAPTCHA Solver

### 浏览器模式（免费）

默认使用浏览器内点击 Turnstile 复选框，配合 `playwright-stealth` 反检测。适合前台模式运行。

```python
CAPTCHA_SOLVER = "browser"
```

### CapSolver（付费）

如果免费模式不稳定，可使用 [capsolver.com](https://www.capsolver.com/) 付费 API，更可靠。

```python
CAPTCHA_SOLVER = "capsolver"
CAPSOLVER_API_KEY = "CAP-xxx"
```

## 输出

注册成功的账户信息保存在 `api_keys.md`，格式：

```
邮箱,密码,API Key,时间;
```

## 常见问题 / FAQ

**Q: 浏览器启动失败？**
A: 确保已运行 `playwright install firefox`。

**Q: Turnstile 解决失败？**
A: 免费模式请使用前台模式运行（`HEADLESS = False`）。如果仍失败，切换到 `CAPTCHA_SOLVER = "capsolver"`。

**Q: 收不到验证邮件？**
A: Cloudflare 模式检查 Worker 是否正常工作；DuckMail 模式检查 Bearer Token。

## License

MIT
