import socket
import time
import hashlib
from Cryptodome.Cipher import AES

# 填入你剛剛挖到的寶藏
DEVICE_IP = "192.168.1.113"
TOKEN = "RwqVP0uAN2fw9w1V"

def get_miio_key_iv(token_bytes):
    key = hashlib.md5(token_bytes).digest()
    iv = hashlib.md5(key + token_bytes).digest()
    return key, iv

def miio_command(method, params=[]):
    token_bytes = TOKEN.encode()
    key, iv = get_miio_key_iv(token_bytes)
    
    # 1. 準備 Hello 封包 (32 bytes)
    hello_pkt = bytes.fromhex('21310020ffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    
    try:
        # 握手：獲取設備當前時間戳與 ID
        sock.sendto(hello_pkt, (DEVICE_IP, 54321))
        data, addr = sock.recvfrom(1024)
        
        did = data[8:12]
        stamp = data[12:16]
        print(f"✅ 握手成功! Device ID: {did.hex()}, Timestamp: {stamp.hex()}")

        # 2. 構建加密指令
        import json
        msg = json.dumps({"id": int(time.time()), "method": method, "params": params}).encode()
        
        # PKCS7 Padding
        pad = 16 - (len(msg) % 16)
        msg += bytes([pad] * pad)
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_msg = cipher.encrypt(msg)
        
        # 3. 封裝 MiIO 封包
        header = bytearray(bytes.fromhex('2131'))
        length = 32 + len(encrypted_msg)
        header.extend(length.to_bytes(2, 'big'))
        header.extend(bytes.fromhex('00000000')) # Unknown
        header.extend(did)
        header.extend(stamp)
        
        # 計算 Checksum
        checksum_payload = header + token_bytes + encrypted_msg
        checksum = hashlib.md5(checksum_payload).digest()
        
        full_pkt = header + checksum + encrypted_msg
        
        # 4. 發送並接收
        sock.sendto(full_pkt, (DEVICE_IP, 54321))
        res_data, res_addr = sock.recvfrom(4096)
        
        # 5. 解密回覆 (跳過 32 bytes header)
        cipher_res = AES.new(key, AES.MODE_CBC, iv)
        decrypted_res = cipher_res.decrypt(res_data[32:])
        print(f"📩 回傳數據: {decrypted_res.decode('utf-8', errors='ignore')}")

    except Exception as e:
        print(f"❌ 錯誤: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    # 測試：查詢狀態
    miio_command("get_status")
    # 想測試讓它叫一聲找它？解鎖下面這行：
    # miio_command("find_me")
