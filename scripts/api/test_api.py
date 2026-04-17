#!/usr/bin/env python3
"""
Test Valetudo REST API and MiIO UDP Protocol
"""

import socket
import json
import time
import hashlib
import struct
from typing import Any, Dict, Optional

ROBOT_IP = "192.168.1.51"
MIIO_PORT = 54321
TOKEN = "aFym5l1XUcKQMav5"

class MiIOClient:
    """MiIO UDP 協定的簡單實現"""
    
    MAGIC = 0x2131
    
    def __init__(self, ip: str, token: str):
        self.ip = ip
        self.token = token.encode('utf-8')
        self.device_id = None
        self.stamp = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5)
        
    def _md5(self, data: bytes) -> bytes:
        return hashlib.md5(data).digest()
    
    def _encrypt(self, data: bytes) -> bytes:
        result = bytearray(len(data))
        for i, b in enumerate(data):
            result[i] = b ^ self.token[i % 32]
        return bytes(result)
    
    def _decrypt(self, data: bytes) -> bytes:
        return self._encrypt(data)
    
    def _build_packet(self, payload: bytes) -> bytes:
        self.stamp = int(time.time()) & 0xFFFFFFFF
        payload_len = len(payload)
        packet_len = 32 + payload_len
        
        header = bytearray(32)
        header[0:2] = struct.pack('<H', self.MAGIC)      # Magic
        header[2:4] = struct.pack('<H', packet_len)       # Length
        header[4:8] = struct.pack('<I', 0)                 # Unknown
        header[8:12] = struct.pack('<I', self.device_id or 0)  # Device ID
        header[12:16] = struct.pack('<I', self.stamp)       # Stamp
        header[16:48] = self.token                          # Token
        
        full_data = bytes(header) + payload
        checksum = self._md5(full_data)
        
        encrypted = self._encrypt(payload)
        return bytes(header) + encrypted + checksum
    
    def _parse_hello(self, data: bytes):
        if len(data) < 32:
            return None
        self.device_id = struct.unpack('<I', data[8:12])[0]
        return self.device_id
    
    def _parse_response(self, data: bytes) -> Optional[Dict[str, Any]]:
        if len(data) < 32:
            return None
        
        packet_len = struct.unpack('<H', data[2:4])[0]
        if len(data) < packet_len:
            return None
        
        self.device_id = struct.unpack('<I', data[8:12])[0]
        
        payload_len = packet_len - 32 - 16
        if payload_len <= 0:
            return None
        
        encrypted = data[32:32+payload_len]
        decrypted = self._decrypt(encrypted)
        
        try:
            return json.loads(decrypted.decode('utf-8'))
        except:
            return None
    
    def hello(self) -> bool:
        """發送 Hello 握手"""
        payload = b''
        packet_len = 32 + len(payload)
        
        header = bytearray(32)
        header[0:2] = struct.pack('<H', self.MAGIC)
        header[2:4] = struct.pack('<H', packet_len)
        header[4:8] = struct.pack('<I', 0xFFFFFFFF)  # Hello marker
        header[8:12] = struct.pack('<I', 0)
        header[12:16] = struct.pack('<I', int(time.time()))
        header[16:48] = b'\xFF' * 32  # Empty token for hello
        
        self.sock.sendto(bytes(header), (self.ip, MIIO_PORT))
        
        try:
            resp, _ = self.sock.recvfrom(4096)
            self._parse_hello(resp)
            return True
        except socket.timeout:
            return False
    
    def send(self, method: str, params: Any = None) -> Optional[Dict[str, Any]]:
        """發送命令並接收回應"""
        msg_id = int(time.time() * 1000) % 0x7FFFFFFF
        
        payload_data = {
            "id": msg_id,
            "method": method,
            "params": params if params is not None else []
        }
        
        payload = json.dumps(payload_data).encode('utf-8')
        packet = self._build_packet(payload)
        
        self.sock.sendto(packet, (self.ip, MIIO_PORT))
        
        try:
            resp, _ = self.sock.recvfrom(4096)
            return self._parse_response(resp)
        except socket.timeout:
            return None
    
    def close(self):
        self.sock.close()


def test_rest_api():
    """測試 Valetudo REST API"""
    import urllib.request
    import urllib.error
    
    base_url = f"http://{ROBOT_IP}"
    
    print("=" * 60)
    print("REST API 測試 (Valetudo)")
    print("=" * 60)
    
    endpoints = [
        ("/api/v2/robot/capabilities", "GET", None),
        ("/api/v2/robot/state/attributes", "GET", None),
        ("/api/v2/robot/capabilities/ConsumableMonitoringCapability", "GET", None),
        ("/api/v2/robot/capabilities/TotalStatisticsCapability", "GET", None),
        ("/api/v2/robot/capabilities/LocateCapability", "PUT", {"action": "locate"}),
        ("/api/v2/robot/capabilities/FanSpeedControlCapability/preset", "PUT", {"name": "medium"}),
        ("/api/v2/robot/capabilities/BasicControlCapability", "PUT", {"action": "home"}),
    ]
    
    for path, method, data in endpoints:
        url = base_url + path
        try:
            if method == "GET":
                with urllib.request.urlopen(url, timeout=5) as resp:
                    result = resp.read().decode('utf-8')
                    if len(result) > 200:
                        result = result[:200] + "..."
                    print(f"\n✓ GET {path}")
                    print(f"  {result}")
            else:
                req = urllib.request.Request(url, 
                    data=json.dumps(data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    result = resp.read().decode('utf-8')
                    print(f"\n✓ PUT {path} -> {result}")
        except Exception as e:
            print(f"\n✗ {method} {path} -> ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("REST API 測試完成")
    print("=" * 60)


def test_miio_protocol():
    """測試 MiIO UDP 協定"""
    print("\n" + "=" * 60)
    print("MiIO UDP 協定測試")
    print("=" * 60)
    
    client = MiIOClient(ROBOT_IP, TOKEN)
    
    # Hello handshake
    print("\n1. 發送 Hello 握手...")
    if client.hello():
        print(f"   ✓ 握手成功, Device ID: {client.device_id}")
    else:
        print("   ✗ 握手超時")
        client.close()
        return
    
    # Test commands
    commands = [
        ("get_status", None, "取得設備狀態"),
        ("miIO.info", None, "取得 MiIO 資訊"),
        ("get_consumable_status", None, "取得消耗品狀態"),
    ]
    
    for method, params, desc in commands:
        print(f"\n2. {desc} ({method})...")
        result = client.send(method, params)
        if result:
            print(f"   ✓ 回應:")
            print(f"   {json.dumps(result, indent=4)[:500]}")
        else:
            print(f"   ✗ 無回應或解析失敗")
    
    # Test control
    print(f"\n3. 測試控制命令...")
    
    print("   設定風扇速度 60%...")
    result = client.send("set_fan_speed", [60])
    print(f"   結果: {result}")
    
    print("   開始清掃 (app_start)...")
    result = client.send("app_start")
    print(f"   結果: {result}")
    
    time.sleep(2)
    
    print("   暫停清掃 (app_pause)...")
    result = client.send("app_pause")
    print(f"   結果: {result}")
    
    time.sleep(1)
    
    print("   返回充電座 (app_charge)...")
    result = client.send("app_charge")
    print(f"   結果: {result}")
    
    # Get final status
    print("\n4. 取得最終狀態...")
    result = client.send("get_status")
    if result:
        print(f"   狀態: {result}")
    
    client.close()
    print("\n" + "=" * 60)
    print("MiIO 協定測試完成")
    print("=" * 60)


if __name__ == "__main__":
    print("Roborock V1 API 測試腳本")
    print(f"目標設備: {ROBOT_IP}")
    print(f"Token: {TOKEN[:8]}...{TOKEN[-4:]}")
    print()
    
    test_rest_api()
    test_miio_protocol()
