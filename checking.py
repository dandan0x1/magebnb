import threading
from web3 import Web3

# 初始化 RPC 连接（MegaBNB 测试链）
w3 = Web3(Web3.HTTPProvider("https://rpc.mbscan.io"))

if not w3.is_connected():
    print("❌ 无法连接到 MegaBNB 测试链 RPC")
    exit(1)

# 读取地址
input_file = r"D:\web3\dan\magebnb-main\2000dz.txt"
output_file = r"D:\web3\dan\magebnb-main\balances.txt"

with open(input_file, "r", encoding="utf-8") as f:
    addresses = [line.strip() for line in f if line.strip()]

# 用于线程写入和统计的锁
lock = threading.Lock()

# 存储所有余额信息和总数
results = []
total_balance = 0


def query_worker(sub_addresses, thread_id):
    global total_balance
    for idx, addr in enumerate(sub_addresses, start=1):
        try:
            checksum_addr = Web3.to_checksum_address(addr)
            balance_wei = w3.eth.get_balance(checksum_addr)
            balance_bnb = w3.from_wei(balance_wei, "ether")

            with lock:
                results.append(f"{addr},{balance_bnb} BNB")
                total_balance += float(balance_bnb)
                print(f"[线程 {thread_id}] 地址: {addr} | 余额: {balance_bnb} BNB")
        except Exception as e:
            with lock:
                results.append(f"{addr},查询失败")
                print(f"[线程 {thread_id}] 查询失败: {addr} | 错误: {e}")


# 分成 5 组地址
thread_count = 5
batch_size = (len(addresses) + thread_count - 1) // thread_count
threads = []

for i in range(thread_count):
    start = i * batch_size
    end = min((i + 1) * batch_size, len(addresses))
    sublist = addresses[start:end]
    t = threading.Thread(target=query_worker, args=(sublist, i + 1))
    threads.append(t)
    t.start()

# 等待线程完成
for t in threads:
    t.join()

# 写入文件
with open(output_file, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(results))

print("\n✅ 所有地址余额查询完成！")
print(f"📊 总余额为：{total_balance:.6f} BNB")
