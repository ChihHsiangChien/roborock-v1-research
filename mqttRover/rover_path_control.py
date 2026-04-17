import paho.mqtt.client as mqtt
import zlib, json, requests, time, math
import argparse

# === 集中配置區 ===
CONFIG = {
    "ROBOT_IP": "192.168.1.113",
    "MQTT_BROKER": "localhost",
    "MQTT_PORT": 1883,
    "MQTT_TOPIC": "valetudo/Rover/#",
    "GOTO_TIMEOUT": 5,
    "ARRIVE_THRESHOLD": 12,    # 判定抵達的距離閾值
    "STUCK_THRESHOLD": 6,      # 座標連續不變的次數 (約 3 秒)
    "PROGRESS_TIMEOUT": 10,    # 距離目標的最小值若超過此秒數未更新，視為無進展
    "POINT_MAX_TIME": 40,      # 單一目標點的最長容忍時間 (秒)
}

class RoverController:
    def __init__(self):
        self.x, self.y = None, None
        self.found_coords = False
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        self.goto_url = f"http://{CONFIG['ROBOT_IP']}/api/v2/robot/capabilities/GoToLocationCapability"

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
            res = requests.put(self.goto_url, json=payload, timeout=CONFIG['GOTO_TIMEOUT'])
            return res.status_code == 200
        except: return False

    def connect(self):
        try:
            self.client.connect(CONFIG['MQTT_BROKER'], CONFIG['MQTT_PORT'])
            self.client.subscribe(CONFIG['MQTT_TOPIC'])
            print("🛰️  正在獲取初始座標...")
            return self.wait_for_pos()
        except Exception as e:
            print(f"❌ 連接失敗: {e}")
            return None, None

    def execute_path(self, path):
        for i, (tx, ty) in enumerate(path):
            print(f"\n--- 🌀 頂點 {i+1} / {len(path)} ---")
            
            if self.x is not None:
                if math.hypot(self.x - tx, self.y - ty) < CONFIG['ARRIVE_THRESHOLD']:
                    print("📍 已在目標附近，跳過...")
                    continue

            if self.goto(tx, ty):
                start_time = time.time()
                last_pos = (0, 0)
                stuck_count = 0
                
                min_dist = float('inf')
                last_progress_time = time.time()
                
                while True:
                    nx, ny = self.wait_for_pos()
                    if nx is None: continue
                    
                    now = time.time()
                    dist = math.hypot(nx - tx, ny - ty)
                    print(f"🏃 移動中... 當前: ({nx}, {ny}), 剩餘: {dist:.1f}")
                    
                    # 1. 成功抵達
                    if dist < CONFIG['ARRIVE_THRESHOLD']:
                        print(f"✅ 抵達頂點 {i+1}")
                        break
                    
                    # 2. 總超時判定
                    if (now - start_time) > CONFIG['POINT_MAX_TIME']:
                        print(f"⏰ 單點執行超時 ({CONFIG['POINT_MAX_TIME']}s)，放棄此點。")
                        break

                    # 3. 座標停滯判定 (物理卡死)
                    if (nx, ny) == last_pos:
                        stuck_count += 1
                    else:
                        stuck_count = 0
                    last_pos = (nx, ny)

                    if stuck_count >= CONFIG['STUCK_THRESHOLD']:
                        print(f"⚠️ 偵測到座標長時間無變化 ({stuck_count} 次)，可能無法到達，放棄此點。")
                        break
                    
                    # 4. 進度停滯判定 (打滑或繞圈)
                    if dist < min_dist:
                        min_dist = dist
                        last_progress_time = now
                    elif (now - last_progress_time) > CONFIG['PROGRESS_TIMEOUT']:
                        print(f"🚧 偵測到距離目標無進展 (超過 {CONFIG['PROGRESS_TIMEOUT']}s)，放棄此點。")
                        break
                    
                    time.sleep(0.5)
                time.sleep(1) 
            else:
                print("❌ API 指令失敗，中斷任務")
                break


def get_path(shape, sx, sy, size):
    """路徑產生器：所有形狀皆以目前座標為起點並回到起點"""
    path = []
    if shape == "square":
        path = [
            (sx + size, sy),
            (sx + size, sy + size),
            (sx, sy + size),
            (sx, sy)
        ]
    elif shape in ["octagon", "circle"]:
        sides = 8 if shape == "octagon" else 16
        radius = size
        # 為了讓起點落在圓周上並從當前位置開始，計算圓心
        center_x, center_y = sx - radius, sy
        
        # 產生頂點 (從 1 開始，因為 0 是起點 sx, sy)
        for i in range(1, sides):
            angle = math.radians((360 / sides) * i)
            path.append((center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)))
        
        # 最後強制回到起點
        path.append((sx, sy))
        
    return path

def main():
    parser = argparse.ArgumentParser(description="Rover 通用路徑控制")
    parser.add_argument("--shape", choices=["square", "octagon", "circle"], default="square", help="形狀名稱")
    parser.add_argument("--size", type=int, default=80, help="正方形邊長或圓形半徑")
    args = parser.parse_args()

    rover = RoverController()
    sx, sy = rover.connect()
    
    if sx is None:
        print("❌ 逾時：抓不到座標。請確保機器人在線或手動移動它。")
        return
    
    print(f"🚩 起點鎖定：({sx}, {sy})")
    path = get_path(args.shape, sx, sy, args.size)

    if not path:
        print("❌ 無效的路徑設定")
        return

    print(f"🚀 開始執行 {args.shape} 巡航 (大小: {args.size})...")
    rover.execute_path(path)
    print(f"\n🏆 {args.shape} 巡航完成！")

if __name__ == "__main__":
    main()
