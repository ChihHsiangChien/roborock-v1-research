import socket
import time
import hashlib
import json
import re
from Cryptodome.Cipher import AES

# === 配置區 ===
DEVICE_IP = "192.168.1.113"
TOKEN = "RwqVP0uAN2fw9w1V"

def clean_number(value):
    try:
        if isinstance(value, (int, float)): return float(value)
        num_str = re.search(r"[-+]?\d*\.\d+|\d+", str(value))
        return float(num_str.group()) if num_str else 0.0
    except: return 0.0

def miio_command(method, params=[]):
    token_bytes = TOKEN.encode()
    key = hashlib.md5(token_bytes).digest()
    iv = hashlib.md5(key + token_bytes).digest()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3.0)
    try:
        # 握手
        sock.sendto(bytes.fromhex('21310020ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'), (DEVICE_IP, 54321))
        data, _ = sock.recvfrom(1024)
        did, stamp = data[8:12], data[12:16]

        # 指令
        msg = json.dumps({"id": int(time.time()), "method": method, "params": params}).encode()
        pad = 16 - (len(msg) % 16)
        msg += bytes([pad] * pad)
        encrypted_msg = AES.new(key, AES.MODE_CBC, iv).encrypt(msg)
        
        header = bytearray(bytes.fromhex('2131'))
        header.extend((32 + len(encrypted_msg)).to_bytes(2, 'big'))
        header.extend(bytes.fromhex('00000000'))
        header.extend(did)
        header.extend(stamp)
        
        checksum = hashlib.md5(header + token_bytes + encrypted_msg).digest()
        sock.sendto(header + checksum + encrypted_msg, (DEVICE_IP, 54321))
        
        res_data, _ = sock.recvfrom(4096)
        decrypted = AES.new(key, AES.MODE_CBC, iv).decrypt(res_data[32:])
        raw_str = decrypted.decode('utf-8', errors='ignore')
        return json.loads(raw_str[:raw_str.rfind('}')+1])
    except: return {"error": "timeout"}
    finally: sock.close()

def run_diagnostics():
    print(f"🚀 正在挖掘 Rover 的隱藏歷史...")
    print("="*50)

    # 嘗試獲取總結 (這是目前石頭機器人最常用的歷史指令)
    summary = miio_command("get_clean_summary")
    if "result" in summary:
        res = summary["result"]
        # get_clean_summary 回傳格式通常是: [總時間, 總面積, 總次數, [最近清掃ID列表]]
        print(f"🏅 [挖掘成功 - 歷史總帳]")
        print(f" - 累計運行: {clean_number(res[0])/3600:.1f} 小時")
        print(f" - 累計面積: {clean_number(res[1])/1000000:.2f} ㎡")
        print(f" - 累計次數: {clean_number(res[2])} 次")
        if len(res) > 3:
            print(f" - 最近一次任務 ID: {res[3][0] if res[3] else '無'}")
    else:
        # 如果 summary 失敗，再試一次 get_stat (避免之前是因解析出錯)
        stats = miio_command("get_stat")
        print(f"📊 [get_stat 原始數據]: {stats.get('result', '讀取失敗')}")

if __name__ == "__main__":
    run_diagnostics()
