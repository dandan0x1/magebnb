import requests
import random
import json
import time

# 读取代理地址从 proxy.txt 文件
proxy_list = []
try:
    with open('proxy.txt', 'r') as file:
        proxy_list = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print("proxy.txt 文件未找到！")
    exit(1)

# 读取钱包地址从 wallets.txt 文件
wallet_addresses = []
try:
    with open('wallets.txt', 'r') as file:
        wallet_addresses = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print("wallets.txt 文件未找到！")
    exit(1)

# 请求头
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.megabnb.world',
    'priority': 'u=1, i',
    'referer': 'https://www.megabnb.world/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

# 无限循环
url = 'https://mbscan.io/airdrop'
while True:
    for address in wallet_addresses:
        # 随机选择一个代理
        proxy = random.choice(proxy_list)
        proxies = {
            'http': proxy,
            'https': proxy
        }
        
        data = {
            'address': address
        }
        
        try:
            print(f"地址: {address} | 使用代理: {proxy}")
            response = requests.post(url, headers=headers, json=data, proxies=proxies, timeout=10)
            print(f"状态码: {response.status_code}")
            
            # 解析响应
            try:
                response_json = response.json()
                if response_json.get('success', False):
                    amount = response_json.get('amount', 0)
                    tx_hash = response_json.get('tx_hash', 'N/A')
                    print(f"领取成功！金额: {amount} wei | 交易哈希: {tx_hash}")
                    # 保存成功结果到文件
                    with open('success.txt', 'a') as f:
                        f.write(f"{address},{amount},{tx_hash}\n")
                else:
                    print(f"领取失败: {response_json}")
            except json.JSONDecodeError:
                print(f"响应非 JSON 格式: {response.text}")
            
            print("\n")
        except requests.RequestException as e:
            print(f"请求失败: {e}\n")
        
        # 每次请求后稍作延迟，避免请求过于频繁
        time.sleep(1)
    
    # 每轮循环结束后稍作延迟
    print("完成一轮循环，休息 5 秒...")
    time.sleep(5)