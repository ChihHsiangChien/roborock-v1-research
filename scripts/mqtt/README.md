# Rover MQTT 巡航控制

這是一個用於控制 Valetudo 掃地機器人執行特定幾何形狀巡航的工具。它結合了 MQTT 座標回饋與 REST API 指令，具備穩健的停滯偵測與自動放棄機制。

## 🚀 主要功能
- **多種幾何形狀**：支援正方形 (`square`)、八邊形 (`octagon`) 與圓形 (`circle`)。
- **自動回航**：所有路徑最終都會回到初始出發點。
- **配置集中化**：IP、MQTT 主題與超時設定皆集中在 `CONFIG` 區塊。
- **穩健移動邏輯**：
  - **停滯偵測**：若座標連續 3 秒無變化，自動跳過該點。
  - **進度監控**：若 10 秒內未靠近目標，視為受阻並跳過。
  - **超時保護**：單一目標點執行超過 40 秒自動放棄。

## 🛠️ 環境需求
- Python 3.x
- 相關套件：`paho-mqtt`, `requests`
- 掃地機器人需安裝 **Valetudo** 韌體並開啟 MQTT 與 GoToCapability。

## 📦 安裝
```bash
pip install paho-mqtt requests
```

## 📖 使用方式

### 1. 修改配置
在 `rover_path_control.py` 的 `CONFIG` 區塊中設定您的機器人 IP 與 MQTT 伺服器資訊：
```python
CONFIG = {
    "ROBOT_IP": "192.168.1.113",
    "MQTT_BROKER": "localhost",
    # ...
}
```

### 2. 執行指令

**執行正方形巡航 (預設)：**
```bash
python rover_path_control.py --shape square --size 80
```

**執行八邊形巡航：**
```bash
python rover_path_control.py --shape octagon --size 100
```

**執行圓形 (16邊形) 巡航：**
```bash
python rover_path_control.py --shape circle --size 120
```

## 檔案說明
- `rover_path_control.py`: 主控制程式。
- `rover_mqtt_square.py`: 方形巡航 (原始參考檔)。
- `rover_mqtt_octagon.py`: 八邊形巡航 (原始參考檔)。
- `clean_coords.py`: 座標清理工具。
