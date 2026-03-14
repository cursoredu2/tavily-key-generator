"""
配置文件 - 复制为 config.py 并填写你的信息
cp config.example.py config.py
"""

# 邮箱后端: "cloudflare" 或 "duckmail"
EMAIL_PROVIDER = "cloudflare"

# ═══ Cloudflare Email Worker (EMAIL_PROVIDER = "cloudflare" 时必填) ═══
EMAIL_DOMAIN = ""           # 你的域名，如 example.com
EMAIL_PREFIX = "tavily"     # 邮箱前缀，生成如 tavily-abc12345@example.com
EMAIL_API_URL = ""          # Email Worker URL，如 https://mail.example.com
EMAIL_API_TOKEN = ""        # Email Worker API Token

# ═══ DuckMail (EMAIL_PROVIDER = "duckmail" 时必填) ═══
DUCKMAIL_API_BASE = "https://api.duckmail.sbs"
DUCKMAIL_BEARER = ""        # DuckMail API Key (dk_xxx)
DUCKMAIL_DOMAIN = "duckmail.sbs"

# ═══ CapSolver (解决 Cloudflare Turnstile 验证码) ═══
CAPSOLVER_API_KEY = ""      # 从 capsolver.com 获取

# ═══ 注册配置 ═══
DEFAULT_PASSWORD = "TavilyAuto123!"
API_KEYS_FILE = "api_keys.md"

# ═══ 等待时间（秒） ═══
WAIT_TIME_SHORT = 2
WAIT_TIME_MEDIUM = 5
WAIT_TIME_LONG = 10
EMAIL_CHECK_INTERVAL = 10
MAX_EMAIL_WAIT_TIME = 300   # 5分钟

# ═══ 浏览器 ═══
HEADLESS = False            # True = 后台运行
BROWSER_TIMEOUT = 30000     # 30秒
BROWSER_TYPE = "firefox"    # 可选: "chromium", "firefox", "webkit"

# ═══ Tavily ═══
TAVILY_HOME_URL = "https://app.tavily.com/home"
TAVILY_SIGNUP_URL = "https://app.tavily.com/home"
