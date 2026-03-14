#!/usr/bin/env python3
"""
Tavily API Key 自动注册工具
"""
import time
from intelligent_tavily_automation import IntelligentTavilyAutomation
from config import EMAIL_PROVIDER, HEADLESS


def get_run_config():
    """获取运行配置"""
    print("\n⚙️ 运行配置")
    print("-" * 30)

    print("🖥️ 浏览器模式:")
    print("1. 前台模式 (可观察过程)")
    print("2. 后台模式 (更快)")

    while True:
        browser_choice = input("选择浏览器模式 (1/2): ").strip()
        if browser_choice in ['1', '2']:
            headless = browser_choice == '2'
            break
        print("❌ 请输入 1 或 2")

    while True:
        try:
            count = int(input("\n📊 注册账户数量 (1-10): "))
            if 1 <= count <= 10:
                break
            print("❌ 请输入 1-10 之间的数字")
        except ValueError:
            print("❌ 请输入有效数字")

    return headless, count


def run_batch(headless, count, email_prefix=None):
    """批量注册"""
    success_count = 0

    for i in range(count):
        print(f"\n{'='*60}")
        print(f"🔄 注册第 {i+1}/{count} 个账户")
        print(f"{'='*60}")

        automation = None
        try:
            automation = IntelligentTavilyAutomation()
            automation.email_prefix = email_prefix
            automation.start_browser(headless=headless)

            start_time = time.time()
            api_key = automation.run_complete_automation()
            elapsed = time.time() - start_time

            if api_key:
                print(f"🎉 第 {i+1} 个账户注册成功!")
                print(f"⏱️ 耗时: {elapsed:.1f} 秒")
                print(f"📧 邮箱: {automation.email}")
                print(f"🔑 API Key: {api_key}")
                success_count += 1
            else:
                print(f"❌ 第 {i+1} 个账户注册失败")

        except Exception as e:
            print(f"❌ 第 {i+1} 个账户出错: {e}")
        finally:
            if automation:
                try:
                    automation.close_browser()
                except:
                    pass

    print(f"\n{'='*60}")
    print(f"🎉 批量注册完成!")
    print(f"📊 成功率: {success_count}/{count} ({success_count/count*100:.1f}%)")
    print(f"📄 API Key 已保存到 api_keys.md")
    print(f"{'='*60}")


def main():
    print("🚀 Tavily API Key 自动注册工具")
    print("=" * 60)
    print(f"📮 邮箱后端: {EMAIL_PROVIDER}")

    while True:
        print("\n🎛️ 选择操作:")
        print("1. 开始批量注册")
        print("2. 退出")

        choice = input("\n请选择 (1-2): ").strip()

        if choice == '1':
            headless, count = get_run_config()

            # Cloudflare 模式下允许自定义前缀
            email_prefix = None
            if EMAIL_PROVIDER == "cloudflare":
                from config import EMAIL_PREFIX
                custom_prefix = input(f"\n📧 邮箱前缀 (回车使用默认 '{EMAIL_PREFIX}'): ").strip()
                email_prefix = custom_prefix if custom_prefix else EMAIL_PREFIX

            print(f"\n📋 配置:")
            print(f"  邮箱后端: {EMAIL_PROVIDER}")
            if email_prefix:
                print(f"  邮箱前缀: {email_prefix}")
            print(f"  浏览器: {'后台' if headless else '前台'}模式")
            print(f"  数量: {count} 个")

            if input("\n🚀 开始? (y/n): ").lower().strip() == 'y':
                run_batch(headless, count, email_prefix)

            if input("\n继续? (y/n): ").lower().strip() != 'y':
                break
        elif choice == '2':
            break
        else:
            print("❌ 无效选择")

    print("👋 再见!")


if __name__ == "__main__":
    main()
