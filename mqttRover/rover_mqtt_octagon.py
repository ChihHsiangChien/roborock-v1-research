import paho.mqtt.client as mqtt
import zlib, json, requests, time, math

# === 配置區 ===
ROBOT_IP = "192.168.1.113"
MQTT_BROKER = "localhost"
MQTT_TOPIC = "valetudo/Rover/#"
GOTO_URL = f"http://{ROBOT_IP}/api/v2/robot/capabilities/GoToLocationCapability"

class RoverOctagon:
    def __init__(self):
        self.x, self.y, self.found_coords = None, None, False
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        if "map-data" in msg.topic:
            try:
                data = json.loads(zlib.decompress(msg.payload))
                for entity in data.get('entities', []):
                    if entity.get('type') == 'robot_position':
                        self.x, self.y = entity['points'][0], entity['points'][1]
                        self.found_coords = True
            except: pass

    def wait_for_pos(self, timeout=20):
        self.found_coords = False
        start_time = time.time()
        while not self.found_coords and (time.time() - start_time) < timeout:
            self.client.loop(0.1)
        return self.x, self.y

    def goto(self, tx, ty):
        print(f"🎯 目標設定：({int(tx)}, {int(ty)})")
        payload = {"action": "goto", "coordinates": {"x": int(tx), "y": int(ty)}}
        try:
            res = requests.put(GOTO_URL, json=payload, timeout=5)
            return res.status_code == 200
        except: return False

def main():
    rover = RoverOctagon()
    rover.client.connect(MQTT_BROKER, 1883)
    rover.client.subscribe(MQTT_TOPIC)

    print("🛰️  獲取初始座標...")
    sx, sy = rover.wait_for_pos()
    if sx is None: return
    
    print(f"🚩 起點鎖定：({sx}, {sy})")

    R = 80 # 稍微放大半徑，移動感會更強
    center_x, center_y = sx - R, sy
    path = []
    for i in range(8):
        angle = math.radians(45 * i)
        path.append((center_x + R * math.cos(angle), center_y + R * math.sin(angle)))

    for i, (tx, ty) in enumerate(path):
        print(f"\n--- 🌀 頂點 {i+1} / 8 ---")
        dist_to_start = ((rover.x - tx)**2 + (rover.y - ty)**2)**0.5
        if dist_to_start < 10:
            print("📍 已在目標附近，準備前往下一站...")
            continue

        if rover.goto(tx, ty):
            last_pos = (0, 0)
            stuck_count = 0
            
            while True:
                nx, ny = rover.wait_for_pos()
                dist = ((nx - tx)**2 + (ny - ty)**2)**0.5
                print(f"🏃 移動中... 當前: ({nx}, {ny}), 剩餘: {dist:.1f}")
                
                # 1. 正常抵達判定 (放寬到 12)
                if dist < 12:
                    print(f"✅ 抵達頂點 {i+1}")
                    break
                
                # 2. 停滯判定：如果座標連續 5 次沒變，且距離已經夠近
                if (nx, ny) == last_pos:
                    stuck_count += 1
                else:
                    stuck_count = 0
                last_pos = (nx, ny)

                if stuck_count >= 5 and dist < 20:
                    print(f"⚠️ 偵測到物理停滯 (距離 {dist:.1f})，強行進入下一點。")
                    break
                
                time.sleep(0.5)
            time.sleep(1) # 頂點間稍微停頓
        else:
            print("❌ API 失敗")
            break

    print("\n🏆 八邊形巡航完成！")

if __name__ == "__main__":
    main()
