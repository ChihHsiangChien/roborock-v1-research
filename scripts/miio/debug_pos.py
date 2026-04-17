import socket
import time
import hashlib
import json
from Cryptodome.Cipher import AES

# === 配置區 ===
DEVICE_IP = "192.168.1.113"
TOKEN = "RwqVP0uAN2fw9w1V"

def miio_command(method, params=[]):
    token_bytes = TOKEN.encode()
    key = hashlib.md5(token_bytes).digest()
    iv = hashlib.md5(key + token_bytes).digest()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3.0)
    try:
        # 1. 握手
        sock.sendto(bytes.fromhex('21310020ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'), (DEVICE_IP, 54321))
        data, _ = sock.recvfrom(1024)
        did, stamp = data[8:12], data[12:16]

        # 2. 封裝指令
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
        
        # 3. 接收與解密
        res_data, _ = sock.recvfrom(4096)
        decrypted = AES.new(key, AES.MODE_CBC, iv).decrypt(res_data[32:])
        raw_str = decrypted.decode('utf-8', errors='ignore')
        return json.loads(raw_str[:raw_str.rfind('}')+1])
    except Exception as e:
        return {"error": str(e)}
    finally:
        sock.close()

if __name__ == "__main__":
    print("🔍 正在嘗試多種方式獲取 Rover 座標...")
    
    # 嘗試 1: 直接屬性查詢
    print("\n[方法 1: app_get_prop]")
    print(miio_command("app_get_prop", ["get_current_position"]))
    
    # 嘗試 2: 狀態查詢 (看裡面有沒有 hidden fields)
    print("\n[方法 2: get_status]")
    print(miio_command("get_status"))

    # 嘗試 3: 詢問導航點
    print("\n[方法 3: get_navigation_status]")
    print(miio_command("get_navigation_status"))
