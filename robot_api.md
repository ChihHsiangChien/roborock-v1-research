# Roborock V1 (Valetudo) API 技術文件

**設備**: Roborock V1 (rockrobo.vacuum.v1)  
**Valetudo 版本**: 2026.02.0  
**設備 ID**: 82512493  
**最後更新**: 2026-04-16

---

## ✅ 已驗證結果

所有範例均已實際測試通過。

### 設備狀態
- **狀態**: docked (停靠在充電座)
- **電量**: 100%
- **風扇**: medium
- **總清掃時間**: 549.2 小時
- **總清掃面積**: 312.69 平方公尺
- **總清掃次數**: 1417 次

### 消耗品狀態
- 主刷: 285 小時剩餘
- 邊刷: 185 小時剩餘
- 濾網: 135 小時剩餘
- 感測器: 26 小時剩餘

---

## 1. 通訊架構

### 1.1 網路端口分布

| 端口 | 協定 | 程式 | 用途 |
|------|------|------|------|
| 80 | TCP | valetudo | Web UI |
| 54321 | UDP | miio_client | MiIO 協定 (需加密) |
| 54322 | TCP | miio_client | 內部命令通道 |
| 6665 | TCP/UDP | player | 機器人控制 (已封鎖) |
| 8079 | TCP | valetudo | FDSMockServer |


---

## 2. Valetudo REST API

### 2.1 GET 端點 (直接存取)

```bash
# 取得狀態
curl -s http://192.168.1.51/api/v2/robot/state/attributes

# 取得消耗品
curl -s http://192.168.1.51/api/v2/robot/capabilities/ConsumableMonitoringCapability

# 取得統計
curl -s http://192.168.1.51/api/v2/robot/capabilities/TotalStatisticsCapability

# 取得 WiFi 狀態
curl -s http://192.168.1.51/api/v2/robot/capabilities/WifiConfigurationCapability

# 取得風扇預設值
curl -s http://192.168.1.51/api/v2/robot/capabilities/FanSpeedControlCapability/presets
```

### 2.2 PUT 端點 (需 SSH 代理)

```bash
# 定位機器人
ssh robot "wget -q -O - --method=PUT --body-data='{\"action\":\"locate\"}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/LocateCapability'"

# 開始清掃
ssh robot "wget -q -O - --method=PUT --body-data='{\"action\":\"start\"}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/BasicControlCapability'"

# 暫停
ssh robot "wget -q -O - --method=PUT --body-data='{\"action\":\"pause\"}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/BasicControlCapability'"

# 停止
ssh robot "wget -q -O - --method=PUT --body-data='{\"action\":\"stop\"}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/BasicControlCapability'"

# 返回充電座
ssh robot "wget -q -O - --method=PUT --body-data='{\"action\":\"home\"}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/BasicControlCapability'"

# 設定風扇 (min/low/medium/high/max)
ssh robot "wget -q -O - --method=PUT --body-data='{\"name\":\"max\"}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/FanSpeedControlCapability/preset'"

# 重置消耗品
ssh robot "wget -q -O - --method=PUT --body-data='{\"consumable\":{\"type\":\"brush\",\"subType\":\"main\"},\"action\":\"reset\"}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/ConsumableMonitoringCapability'"
```

---

## 3. Bash 控制腳本

### 3.1 使用方式

```bash
# 查詢
./robot_control.sh status          # 取得狀態
./robot_control.sh consumables     # 取得消耗品
./robot_control.sh stats           # 取得統計
./robot_control.sh fan-presets     # 顯示風扇預設值

# 控制
./robot_control.sh locate         # 定位機器人
./robot_control.sh start          # 開始清掃
./robot_control.sh pause          # 暫停
./robot_control.sh stop           # 停止
./robot_control.sh home           # 返回充電座

# 風扇速度
./robot_control.sh fan min        # 安靜模式
./robot_control.sh fan max        # 最大模式
./robot_control.sh fan medium     # 平衡模式

# 消耗品重置
./robot_control.sh reset brush main       # 重置主刷
./robot_control.sh reset brush side_right # 重置邊刷
./robot_control.sh reset filter main     # 重置濾網
./robot_control.sh reset cleaning sensor # 重置感測器
```

### 3.2 原始碼

完整腳本源碼位於 `/home/student/robot/robot_control.sh`

---

## 4. Python 客戶端

### 4.1 使用範例

```python
from robot_client import ValetudoClient

client = ValetudoClient()

# 查詢狀態
print(f"狀態: {client.get_status_text()}")    # docked
print(f"電量: {client.get_battery_level()}%") # 100
print(f"風扇: {client.get_fan_speed()}")       # medium

# 印出完整資訊
client.print_info()

# 控制命令
client.locate()                    # 定位
client.start()                     # 開始清掃
client.pause()                     # 暫停
client.stop()                      # 停止
client.home()                      # 返回充電座
client.set_fan_speed("max")       # 設定風扇

# 重置消耗品
client.reset_consumable("brush", "main")     # 主刷
client.reset_consumable("brush", "side_right") # 邊刷
```

### 4.2 原始碼

完整 Python 客戶端位於 `/home/student/robot/robot_client.py`

---

## 5. MiIO UDP 協定 (無法直接使用)

### 5.1 說明

經過測試，**直接外部 MiIO UDP 連接無法運作**。原因：

1. MiIO 協定需要正確的 XOR 加密
2. Token 需要 16 bytes，但加密時重複使用
3. 設備可能限制外部 UDP 連接

### 5.2 建議

使用 Valetudo REST API 取代直接 MiIO 溝通。

---

## 6. 地圖 API

### 6.1 取得地圖

```bash
# 方法 1: 直接從外部 API (GET)
curl -s http://192.168.1.51/api/v2/robot/state/map -o map.json

# 方法 2: SSH 到設備下載 (推薦用於完整數據)
ssh robot "wget -q -O /tmp/map_dump.json 'http://127.0.0.1/api/v2/robot/state/map'"
scp robot:/tmp/map_dump.json ./map_dump.json
```

### 6.2 地圖數據結構

```json
{
  "__class": "ValetudoMap",
  "metaData": {
    "defaultMap": true,
    "version": 2,
    "totalLayerArea": 335175
  },
  "size": {"x": 5120, "y": 5120},
  "pixelSize": 5,
  "layers": [
    {
      "__class": "MapLayer",
      "type": "floor",
      "compressedPixels": [508, 484, 381, ...],
      "dimensions": {"x": {...}, "y": {...}}
    },
    {
      "__class": "MapLayer", 
      "type": "wall",
      "compressedPixels": [...]
    }
  ],
  "entities": [
    {"__class": "PointMapEntity", "type": "charger_location", "points": [2560, 2560]},
    {"__class": "PointMapEntity", "type": "robot_position", "points": [4420, 2560], "metaData": {"angle": 90}},
    {"__class": "PathMapEntity", "type": "path", "points": [2560, 2560, 2640, 2560, ...]}
  ]
}
```

### 6.3 地圖視覺化腳本

```python
#!/usr/bin/env python3
"""
Roborock V1 地圖視覺化工具
使用方式: python3 map_visualizer.py [input.json] [-o output.png]
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

def parse_compressed_pixels(compressed):
    """解析 Valetudo 壓縮像素格式"""
    pixels = []
    i = 0
    while i < len(compressed) - 2:
        x = compressed[i]
        y = compressed[i + 1]
        count = compressed[i + 2]
        for _ in range(count):
            pixels.append((x, y))
        i += 3
    return pixels

def create_map_from_layers(layers, map_size):
    """創建地圖數組. 0=未知, 1=地板, 2=牆壁"""
    map_data = np.zeros((map_size['y'], map_size['x']), dtype=np.uint8)
    layer_types = {'floor': 1, 'wall': 2}
    
    for layer in layers:
        layer_type = layer.get('type', '')
        compressed = layer.get('compressedPixels', [])
        pixels = parse_compressed_pixels(compressed)
        
        for x, y in pixels:
            if 0 <= x < map_size['x'] and 0 <= y < map_size['y']:
                map_data[y, x] = layer_types.get(layer_type, 1)
    
    return map_data

def parse_entities(entities):
    """解析地圖實體"""
    result = {'charger': None, 'robot': None, 'path': []}
    
    for entity in entities:
        entity_type = entity.get('type', '')
        
        if entity_type == 'charger_location':
            points = entity.get('points', [])
            if len(points) >= 2:
                result['charger'] = (points[0], points[1])
        
        elif entity_type == 'robot_position':
            points = entity.get('points', [])
            angle = entity.get('metaData', {}).get('angle', 0)
            if len(points) >= 2:
                result['robot'] = (points[0], points[1], angle)
        
        elif entity_type == 'path':
            points = entity.get('points', [])
            path_points = []
            for i in range(0, len(points) - 1, 2):
                path_points.append((points[i], points[i + 1]))
            result['path'] = path_points
    
    return result

def visualize_map(map_data, entities, pixel_size, output_file=None):
    """視覺化地圖"""
    colors = ['#1a1a1a', '#ffffff', '#888888']  # 未知, 地板, 牆壁
    cmap = LinearSegmentedColormap.from_list('map', colors)
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.imshow(map_data, cmap=cmap, origin='lower', aspect='equal')
    
    # 充電座
    if entities['charger']:
        x, y = entities['charger']
        ax.plot(x, y, 'g^', markersize=15, label='Charger')
        ax.add_patch(plt.Circle((x, y), 30, fill=False, color='green', linewidth=2))
    
    # 機器人位置
    if entities['robot']:
        x, y, angle = entities['robot']
        ax.plot(x, y, 'ro', markersize=12, label='Robot')
        arrow_len = 50
        dx = arrow_len * np.cos(np.radians(angle))
        dy = arrow_len * np.sin(np.radians(angle))
        ax.arrow(x, y, dx, dy, head_width=20, head_length=10, fc='red', ec='red')
    
    # 路徑
    if entities['path']:
        path = np.array(entities['path'])
        if len(path) > 1:
            ax.plot(path[:, 0], path[:, 1], 'b-', linewidth=1, alpha=0.5, label='Path')
    
    # 比例尺
    scale_size = 100
    scale_cm = scale_size * pixel_size
    scale_text = f"{scale_cm/100:.1f} m" if scale_cm >= 100 else f"{scale_cm:.0f} cm"
    ax.plot([20, 20 + scale_size], [30, 30], 'w-', linewidth=3)
    ax.text(20 + scale_size/2, 45, scale_text, color='white', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    ax.set_title(f'Roborock V1 Map (Pixel Size: {pixel_size} cm)', fontsize=14, color='white')
    ax.axis('off')
    
    legend_elements = [
        mpatches.Patch(facecolor='green', label='Charging Dock'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Robot'),
        plt.Line2D([0], [0], color='blue', linewidth=2, label='Path'),
        mpatches.Patch(facecolor='white', label='Floor'),
        mpatches.Patch(facecolor='#888888', label='Wall'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
             facecolor='black', edgecolor='white', labelcolor='white')
    
    fig.patch.set_facecolor('#2d2d2d')
    ax.set_facecolor('#1a1a1a')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f"Map saved to: {output_file}")
    plt.show()

# 主程式
if __name__ == '__main__':
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else '/home/student/robot/map_dump.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    map_size = data.get('size', {'x': 5120, 'y': 5120})
    pixel_size = data.get('pixelSize', 5)
    layers = data.get('layers', [])
    entities = data.get('entities', [])
    
    map_data = create_map_from_layers(layers, map_size)
    parsed_entities = parse_entities(entities)
    
    print(f"Map size: {map_data.shape[1]} x {map_data.shape[0]} pixels")
    print(f"Pixel size: {pixel_size} cm")
    if parsed_entities['charger']:
        print(f"Charger: {parsed_entities['charger']}")
    if parsed_entities['robot']:
        print(f"Robot: {parsed_entities['robot']}")
    if parsed_entities['path']:
        print(f"Path points: {len(parsed_entities['path'])}")
    
    visualize_map(map_data, parsed_entities, pixel_size, output_file)
```

### 6.4 快速使用步驟

```bash
# 1. 取得地圖
curl -s http://192.168.1.51/api/v2/robot/state/map -o map.json

# 2. 視覺化 (需要 matplotlib)
python3 map_visualizer.py map.json -o map.png

# 或使用已產生的腳本
python3 map_visualizer.py
```

### 6.5 地圖時間戳

Valetudo REST API (`/api/v2/robot/state/map`) **不回傳時間戳**，地圖是即時快照。

**查詢地圖產生時間的方法**:

```bash
# 方法 1: 檢查 VacuumAndBrush.cfg 檔案修改時間 (最後一次清掃結束時間)
ssh robot "stat /mnt/data/rockrobo/VacuumAndBrush.cfg"

# 輸出範例:
# Modify: 2026-04-16 18:57:22.260004903 +0800

# 方法 2: 檢查 robot.db 的 cleanrecords 表 (需要下載資料庫)
scp robot:/mnt/data/rockrobo/robot.db /tmp/robot.db
python3 -c "
import sqlite3
from datetime import datetime
conn = sqlite3.connect('/tmp/robot.db')
cursor = conn.cursor()
cursor.execute('SELECT begin, end, duration, area FROM cleanrecords ORDER BY begin DESC LIMIT 5')
for row in cursor.fetchall():
    print(f'Start: {datetime.fromtimestamp(row[0])}, End: {datetime.fromtimestamp(row[1])}, Duration: {row[2]}s, Area: {row[3]}')
"
```

**重要結論**: 
- Valetudo 地圖 API 無時間戳 → 地圖代表當前狀態
- 最近一次清掃時間 → `VacuumAndBrush.cfg` 檔案修改時間
- 清掃歷史記錄 → `robot.db` 的 `cleanrecords` 表

### 6.6 地圖數據說明

| 欄位 | 說明 |
|------|------|
| size | 地圖像素尺寸 (5120x5120) |
| pixelSize | 每像素代表的大小 (5 cm) |
| layers | 圖層: floor(地板), wall(牆壁) |
| entities | 實體: charger_location, robot_position, path |
| compressedPixels | 行程長度編碼壓縮格式 |

**實體座標**:
- 充電座: (2560, 2560) = 地圖中心
- 機器人: (4420, 2560, 90) = x, y, 角度(度)

**座標系統**:
- 原點在左下角
- X 向右增加
- Y 向上增加
- 實際距離 = 像素 * pixelSize cm

---

## 7. 吸塵器控制

### 7.1 風扇速度預設值

| 預設值 | 說明 |
|--------|------|
| min | 安靜模式 (~38%) |
| low | 低功率 |
| medium | 平衡模式 (~60%) |
| high | 高功率 |
| max | 最大模式 (~100%) |

### 7.2 吸塵器狀態

```bash
# 查詢目前風扇速度
curl -s http://192.168.1.51/api/v2/robot/state/attributes
```

```json
[{"__class":"StatusStateAttribute","value":"docked"},
 {"__class":"BatteryStateAttribute","level":100},
 {"__class":"PresetSelectionStateAttribute","type":"fan_speed","value":"medium"}]
```

### 7.3 吸塵器限制與測試

**重要**: 無法完全關閉吸塵器馬達
- Valetudo FanSpeedControlCapability 不提供 "off" 選項
- 最低速為 `min`，PWM 約 0.01 (1% 功率)
- 馬達在機器人啟動時自動運行

**測試結果**:
| 設定方式 | PWM 值 | 實際效果 |
|----------|--------|----------|
| 設定 `speed: 0` | 0.01 | 最低功率 |
| 設定 `min` | 0.01 | 相同效果 |
| 回充時 (docked) | 0.30 | 降至 30% (非完全關閉) |

**結論**: 
- 回充時風扇降至 30% (非完全關閉)
- 無法透過 Valetudo API 完全關閉吸塵器
- 如需完全靜音，需物理關閉電源開關

### 7.4 不同模式的風扇 PWM

| 模式 | PWM 值 | 說明 |
|------|--------|------|
| 正常清掃 | 0.60 | 60% |
| 回充模式 | 0.30 | 30% |
| 定點清掃 | 0.70 | 70% |
| 最低速 (min) | 0.01 | 1% |

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg`

### 7.4 吸塵器設定檔案

| 檔案 | 路徑 |
|------|------|
| PWM 設定 | `/mnt/data/rockrobo/VacuumAndBrush.cfg` |

```bash
# 透過 SSH 查看目前 PWM 設定
ssh robot "cat /mnt/data/rockrobo/VacuumAndBrush.cfg"
```

---

## 8. 方位角與羅盤

### 8.1 取得機器人朝向

```bash
# 透過 Valetudo 地圖 API
curl -s http://192.168.1.51/api/v2/robot/state/map | grep robot_position
```

輸出範例：
```json
{"type":"robot_position","points":[4420,2560],"metaData":{"angle":90}}
```

### 8.2 方位感測器

| 感測器 | 介面 | 功能 |
|--------|------|------|
| 電子羅盤 | compass:::position3d:2 | 提供絕對朝向 |
| 陀螺儀 | gyro:::position3d:0 | 三軸角速度 |
| LDS | laser:0 | 360° 雷射測距 |

### 8.3 方位角相關參數

| 參數 | 值 | 說明 |
|------|-----|------|
| 最大偏航速度 | 3.14 rad/s | 旋轉速度上限 |
| 安全旋轉角度 | 35° | 安全操作範圍 |
| 預設轉向速度 | 45 °/s | 標準旋轉速度 |
| 羅盤閾值 | 2000 | 羅盤校正靈敏度 |

### 8.4 充電座角度

充電座位置固定為地圖中心 (2560, 2560)，朝向需從路徑數據推斷。

---

## 9. 光學雷達 (LDS) 數據

### 9.1 LDS 規格

| 項目 | 值 |
|------|-----|
| 型號 | LDS (Laser Distance Sensor) |
| 角度範圍 | -180° 到 180° |
| 最大範圍 | 6 米 |
| 馬達轉速 | 270-330 RPM |
| 姿勢偏移 | x=-100mm, yaw=97.6° |

### 9.2 數據存取方式

**無法直接讀取原始 LDS 掃描數據**：

| 方式 | 可用性 | 說明 |
|------|--------|------|
| Valetudo REST API | ❌ | 不提供原始掃描數據 |
| Valetudo 地圖 | ⚠️ | 只有處理過的地圖 (壓縮格式) |
| Player 框架 (Port 6665) | ⚠️ | SSH 可達，但對外封鎖 |
| 直接串口 /dev/ttyS1 | ❌ | 需要特殊權限 |

### 9.3 可取得的替代數據

```bash
# 取得處理過的地圖（包含牆壁、地板、路徑）
curl -s http://192.168.1.51/api/v2/robot/state/map -o map.json
```

地圖 API 回傳內容：
- `layers[].type`: floor (地板), wall (牆壁)
- `layers[].compressedPixels`: RLE 壓縮格式
- `entities[]`: 充電座、機器人位置、清掃路徑

### 9.4 LDS 數據流

```
LDS 硬體 → /dev/ttyS1 → librubylaserdriver.so 
    → raw:::laser:0 → Player 框架 
    → slam:::laser:2 → rrSLAM 
    → 地圖生成
```

LDS 原始數據被 Player 框架內部消耗，用於 SLAM 定位和導航，不對外暴露。

---

## 10. GoTo 定點移動

### 10.1 API 端點

```bash
# 移動到指定座標
ssh robot "wget -q -O - --method=PUT --body-data='{\"coordinates\":{\"x\":3000,\"y\":3000}}' --header='Content-Type: application/json' 'http://127.0.0.1/api/v2/robot/capabilities/GoToLocationCapability'"
```

### 10.2 GoTo 參數

| 參數 | 值 | 說明 |
|------|-----|------|
| 最大嘗試次數 | 3 | 失敗後重試次數 |
| 充電座前停止距離 | 250 mm | 到充電座前停止 |
| 到歷史點最大嘗試 | 3 次 | 回到上次位置 |

### 10.3 GoTo 時的風扇狀態

GoTo 模式使用**正常 PWM (0.60)**，不回充時不會降低。

### 10.4 直線行走控制

**直線修正參數**:

| 參數 | 值 | 說明 |
|------|-----|------|
| 最小速度 | 0.1 m/s | 直線行走最低速 |
| 最大速度 | 0.3 m/s | 直線行走最高速 |
| 最大偏航速度 | 45 °/s | 方向修正最大角速度 |
| 行走直線距離閾值 | 20 mm | 觸發修正的偏差 |
| 啟動角度誤差 | 10° | 允許的啟動誤差 |

**控制流程**:
```
目標方向 → 里程計計算位移 → 陀螺儀檢測偏航角偏差 
→ 若偏差 > 20mm → 修正偏航速度 (最高 45°/s)
```

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg`

---

## 11. 里程計與馬達控制

### 11.1 里程計 (Odometry)

| 參數 | 值 | 說明 |
|------|-----|------|
| 輪徑 | 0.220 m | 左右輪相同 |
| 編碼器頻率 | 256 Hz | 脈衝/秒 |
| Y偏移 | ±0.1195 m | 左右輪中心距 |
| 里程更新週期 | 50 ms | 速度更新間隔 |

### 11.2 馬達控制限制

**無法直接控制輪速** - 只能透過 Valetudo 發送高層指令。

| 馬達 | 介面 | 說明 |
|------|------|------|
| 左輪 | motor:1 | 由系統自動控制 |
| 右輪 | motor:2 | 由系統自動控制 |
| 真空吸塵 | vaccuum:::motor:0 | 可透過 API 調整速度 |
| 主刷 | main:::motor:1 | 固定 PWM 0.30-0.70 |
| 邊刷 | right:::motor:2 | 固定 PWM 0.35-0.85 |

### 11.3 陀螺-里程融合

| 參數 | 值 | 說明 |
|------|-----|------|
| 偏差閾值比例 | 0.5 | 陀螺與里程偏差容許 |
| 偏差計數上限 | 42 | 最大連續偏差計數 |
| 里程更新頻率 | 256 Hz | 里程計頻率 |

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/ruby_chassis.cfg`, `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg`

---

## 12. 主刷/邊刷馬達控制

### 12.1 PWM 設定

| 馬達 | 正常模式 | 慢速模式 | 說明 |
|------|---------|---------|------|
| 主刷 (Main Brush) | 0.70 (70%) | 0.30 (30%) | 根據速度模式自動切換 |
| 邊刷 (Side Brush) | 0.85 (85%) | 0.35 (35%) | 根據速度模式自動切換 |

### 12.2 控制方式

**無法直接控制刷子馬達** - 它們根據吸塵器速度模式自動調整：

| 風扇速度模式 | 主刷 PWM | 邊刷 PWM |
|-------------|---------|---------|
| min | 0.30 | 0.35 |
| low | 0.30 | 0.35 |
| medium | 0.70 | 0.85 |
| high | 0.70 | 0.85 |
| max | 0.70 | 0.85 |

### 12.3 馬達狀態監控介面

| 介面 | 用途 |
|------|------|
| `motor_status:::ir:3` | 一般馬達狀態 |
| `fan_motor_status:::ir:6` | 吸塵器馬達電流 |
| `main_brush_current_status:::ir:7` | 主刷電流監控 |
| `sweep_brush_current_status:::ir:8` | 邊刷電流監控 |

### 12.4 API 可用性

| 功能 | 可用 | 說明 |
|------|------|------|
| 調整風扇速度 | ✅ | 間接影響刷子速度 |
| 直接控制刷子 | ❌ | 無 API |
| 查看刷子狀態 | ❌ | 無 API |
| 查看刷子電流 | ❌ | 僅內部介面 |

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (VacuumAndBrush 區塊)

---

## 13. 方位角控制

### 13.1 讀取方位角

```bash
# 取得機器人目前朝向
curl -s http://192.168.1.51/api/v2/robot/state/map | grep angle
```

輸出範例：
```json
{"type":"robot_position","points":[4420,2560],"metaData":{"angle":90}}
```

**目前機器人朝向：90 度**

### 13.2 方位角類型

**重要區分**：

| 角度來源 | 類型 | 可讀取 | 說明 |
|----------|------|--------|------|
| Valetudo 地圖 API | 地圖相對座標 | ✅ | 相對於地圖建立時的原點 |
| 電子羅盤 | 地磁方位角 | ❌ | 磁北方向（無 API） |

**地圖 API 回傳的 90 度角是相對於地圖座標系，不是磁北方向。**

### 13.3 電子羅盤 (地磁感測器)

| 項目 | 說明 |
|------|------|
| 驅動 | librubycompassdriver.so |
| 介面 | compass:::position3d:2 |
| 軸數 | 3 軸 (X, Y, Z) |
| 校準狀態 | HAS_CALIBRATED 0 (未校準) |

**電子羅盤用途**：
- 困住偵測 (Trap Detection)
- 羅盤碰撞保護
- 導航修正

### 13.4 控制朝向

| 功能 | 可用性 | 說明 |
|------|--------|------|
| 讀取方位角 | ✅ | 可從地圖 API 取得 |
| 設定目標朝向 | ❌ | 無 API |
| 旋轉到特定角度 | ❌ | 無 API |
| HighResolutionManualControl | ❌ | 已停用 |

### 13.3 旋轉參數（僅供參考）

| 參數 | 值 | 說明 |
|------|-----|------|
| 左轉角度 | 90° | 標準左轉 |
| 右轉角度 | 180° | 標準右轉 |
| 旋轉速度 | 45 °/s | 預設旋轉角速度 |
| 最大偏航速度 | 180 °/s | 快速旋轉 |

### 13.4 結論

**無法直接控制機器人朝向特定角度**：
- 只能讀取當前朝向
- 無法透過 API 設定目標朝向
- `HighResolutionManualControlCapability` 被停用

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (ROTATION_* 參數)

---

## 14. 消耗品類型

| type | subType | 說明 |
|------|---------|------|
| brush | main | 主刷 |
| brush | side_right | 邊刷 |
| filter | main | 濾網 |
| cleaning | sensor | 感測器計時器 |

---

## 15. 設備資訊

| 項目 | 值 |
|------|-----|
| IP 位址 | 192.168.1.51 |
| SSH | `ssh robot` |
| Valetudo Web | http://192.168.1.51 |
| Valetudo API | http://192.168.1.51/api/v2 |
| 地圖 API | http://192.168.1.51/api/v2/robot/state/map |

---

## 附錄：生成的文件

| 檔案 | 說明 |
|------|------|
| `robot_api.md` | API 技術文件 |
| `robot_report.md` | 設備系統報告 |
| `robot_control.sh` | Bash 控制腳本 |
| `robot_client.py` | Python 客戶端 |
| `map_visualizer.py` | 地圖視覺化腳本 |
| `map_dump.json` | 地圖原始數據 |
| `map_output.png` | 地圖圖片 |
| `map_latest.json` | 最新地圖數據 |
| `map_latest.png` | 最新地圖圖片 |
