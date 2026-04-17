import paho.mqtt.client as mqtt
import zlib
import json
import requests
import time

# === 配置區 ===
ROBOT_IP = "192.168.1.113"
MQTT_BROKER = "localhost"
# 訂閱整個 Rover 路徑，確保不漏掉任何座標廣播
MQTT_TOPIC = "valetudo/Rover/#"
GOTO_URL = f"http://{ROBOT_IP}/api/v2/robot/capabilities/GoToLocationCapability"

class RoverMQTTSquare:
    def __init__(self):
        self.x = None
        self.y = None
        self.found_coords = False
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        # 只要是 map-data，我們就解壓來找坐標
        if "map-data" in msg.topic:
            try:
                decompressed = zlib.decompress(msg.payload)
                data = json.loads(decompressed)
                if 'entities' in data:
                    for entity in data['entities']:
                        if entity.get('type') == 'robot_position':
                            self.x = entity['points'][0]
                            self.y = entity['points'][1]
                            self.found_coords = True
            except:
                pass

    def wait_for_pos(self, timeout=20):
        """同步等待 MQTT 傳回座標"""
        self.found_coords = False
        print("🛰️  正在等待 MQTT 座標廣播...")
        start_time = time.time()
        while not self.found_coords and (time.time() - start_time) < timeout:
            self.client.loop(0.1)
        return self.x, self.y

    def goto(self, tx, ty):
        """透過 API 發送指令 (MQTT 負責接收回饋，API 負責下令)"""
        print(f"🎯 目標設定：({tx}, {ty})")
        payload = {"action": "goto", "coordinates": {"x": int(tx), "y": int(ty)}}
        try:
            res = requests.put(GOTO_URL, json=payload, timeout=5)
            return res.status_code == 200
        except:
            return False

def main():
    rover = RoverMQTTSquare()
    rover.client.connect(MQTT_BROKER, 1883)
    rover.client.subscribe(MQTT_TOPIC)

    # 1. 抓初始位置
    curr_x, curr_y = rover.wait_for_pos()
    if curr_x is None:
        print("❌ 逾時：抓不到座標。請在 Valetudo 網頁上手動點一下移動來觸發廣播。")
        return
    
    print(f"🚩 起點鎖定：({curr_x}, {curr_y})")

    # 2. 定義方塊 (移動 50 單位)
    step = 50
    path = [
        (curr_x + step, curr_y),
        (curr_x + step, curr_y + step),
        (curr_x, curr_y + step),
        (curr_x, curr_y)
    ]

    for i, (tx, ty) in enumerate(path):
        print(f"\n--- 階段 {i+1}/4 ---")
        if rover.goto(tx, ty):
            # 閉路監控：直到抵達目標
            while True:
                nx, ny = rover.wait_for_pos()
                dist = ((nx - tx)**2 + (ny - ty)**2)**0.5
                print(f"🏃 移動中... 當前: ({nx}, {ny}), 剩餘距離: {dist:.1f}")
                if dist < 8:
                    print("✅ 已到達頂點！休息中...")
                    time.sleep(3)
                    break
        else:
            print("❌ API 指令失敗")
            break

if __name__ == "__main__":
    main()
