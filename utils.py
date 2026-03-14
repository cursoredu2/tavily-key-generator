"""
工具函数
"""
import time
from datetime import datetime
from config import API_KEYS_FILE


def save_api_key(email, api_key, password=None):
    """保存API key和账户信息到文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    account_line = f"{email},{password if password else 'N/A'},{api_key},{timestamp};\n"

    try:
        with open(API_KEYS_FILE, 'a', encoding='utf-8') as f:
            f.write(account_line)
    except FileNotFoundError:
        with open(API_KEYS_FILE, 'w', encoding='utf-8') as f:
            f.write(account_line)

    print(f"✅ 账户信息已保存到 {API_KEYS_FILE}")
    print(f"📧 邮箱: {email}")
    print(f"🔐 密码: {password if password else 'N/A'}")
    print(f"🔑 API Key: {api_key}")
    print(f"⏰ 时间: {timestamp}")


def wait_with_message(seconds, message="等待中"):
    """带消息的等待函数"""
    print(f"⏳ {message}，等待 {seconds} 秒...")
    time.sleep(seconds)
