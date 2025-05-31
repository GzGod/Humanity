import os
import requests
import random
import time
from datetime import datetime
from colorama import init, Fore

# 初始化彩色终端
init(autoreset=True)

# 文件路径设置
TOKEN_FILE = "tokens.txt"
PROXY_FILE = "proxy.txt"
LOG_FILE = "log.txt"
BASE_URL = "https://testnet.humanity.org"

# 读取 token 列表
if not os.path.exists(TOKEN_FILE):
    print("❌ 未找到 tokens.txt 文件！")
    exit(1)

with open(TOKEN_FILE, "r") as f:
    TOKENS = [line.strip() for line in f if line.strip()]

# 读取代理列表
PROXIES = []
if os.path.exists(PROXY_FILE):
    with open(PROXY_FILE, "r") as f:
        PROXIES = [line.strip() for line in f if line.strip()]

# 获取一个随机代理
def get_proxy():
    if not PROXIES:
        return None
    proxy = random.choice(PROXIES)
    return {"http": proxy, "https": proxy}

# 记录错误日志
def log_error(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

# 封装 API 请求
def api_call(session, endpoint, token, method="POST", payload=None):
    url = BASE_URL + endpoint
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "token": token,
        "user-agent": "Mozilla/5.0"
    }
    try:
        if method == "GET":
            res = session.get(url, headers=headers, timeout=30)
        else:
            res = session.post(url, json=payload or {}, headers=headers, timeout=30)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        raise Exception(f"{endpoint} 请求失败: {str(e)}")

# 单个 token 处理流程
def process_token(token, index):
    proxy = get_proxy()
    session = requests.Session()
    if proxy:
        session.proxies.update(proxy)

    print(Fore.CYAN + f"\n🔹 正在处理 Token #{index + 1}")
    try:
        user_info = api_call(session, "/api/user/userInfo", token)
        print("✅ 用户:", user_info["data"].get("nickName"))
        print("✅ 钱包:", user_info["data"].get("ethAddress"))

        balance = api_call(session, "/api/rewards/balance", token, "GET")
        print(Fore.YELLOW + f"💰 当前积分: {balance['balance']['total_rewards']}")

        check = api_call(session, "/api/rewards/daily/check", token)
        print("📊 状态:", check["message"])
        if not check.get("available"):
            print("⏳ 今日已领取，跳过...")
            return

        claim = api_call(session, "/api/rewards/daily/claim", token)
        if claim.get("data", {}).get("amount"):
            print("🎉 成功领取:", claim["data"]["amount"])
        elif "successfully" in claim.get("message", ""):
            print("🎉 已领取成功")
        else:
            print("❌ 领取返回异常:", claim)
            return

        updated = api_call(session, "/api/rewards/balance", token, "GET")
        print(Fore.GREEN + f"💰 领取后积分: {updated['balance']['total_rewards']}")

    except Exception as e:
        print(Fore.RED + f"❌ 错误: {e}")
        log_error(f"Token #{index + 1} 错误: {e}")

    delay = random.randint(15, 20)
    print(Fore.MAGENTA + f"⏳ 等待 {delay} 秒...\n")
    time.sleep(delay)

# 倒计时功能
def countdown(seconds):
    while seconds > 0:
        h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
        print(f"\r⏳ 距离下一轮: {h:02d}:{m:02d}:{s:02d}", end="")
        time.sleep(1)
        seconds -= 1
    print("\n⏱️ 倒计时结束，重新开始...")

# 主循环
def run_round():
    print(Fore.GREEN + f"\n🚀 开始处理 {len(TOKENS)} 个 Token...")
    for i, token in enumerate(TOKENS):
        process_token(token, i)
    print(Fore.GREEN + "✅ 本轮完成，启动 24 小时倒计时")
    countdown(86400)
    run_round()

# 启动
run_round()
