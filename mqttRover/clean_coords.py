import paho.mqtt.client as mqtt
import zlib
import json

def on_message(client, userdata, msg):
    if "map-data" in msg.topic:
        try:
            # Valetudo 的地圖數據通常是 zlib 壓縮
            # 我們嘗試解壓並尋找其中的 JSON 部分
            decompressed = zlib.decompress(msg.payload)
            # 嘗試尋找座標字串 (這部分視韌體版本可能需要微調)
            data = json.loads(decompressed)
            if 'entities' in data:
                for entity in data['entities']:
                    if entity.get('type') == 'robot_position':
                        print(f"📍 找到座標！ X: {entity['points'][0]}, Y: {entity['points'][1]}")
        except Exception as e:
            # 如果解壓失敗，代表格式可能不同
            pass
    else:
        # 顯示一般的文字訊息
        try:
            print(f"[{msg.topic}] -> {msg.payload.decode('utf-8')}")
        except:
            pass

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("valetudo/Rover/#")

print("🛰️ 啟動二進位解碼監控...")
client.loop_forever()
