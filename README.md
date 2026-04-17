# Roborock V1 機器人研究文件

**設備**: Roborock V1 (rockrobo.vacuum.v1)  
**IP**: 192.168.1.51  
**韌體**: Valetudo 2026.02.0 + 原廠 3.5.8_004018

---

## 文件索引

### 📋 系統報告

| 檔案 | 說明 |
|------|------|
| `robot_report.md` | 完整系統硬體/軟體報告 |
| `robot_api.md` | Valetudo REST API 技術文件 |

### 🔐 安全與隱私

| 檔案 | 說明 |
|------|------|
| `secrets.md` | 敏感資訊 (金鑰、密碼、SSID) - ⚠️ 請勿上傳 |
| `cloud_communication.md` | 原本傳送到 Xiaomi 雲端的資料分析 |
| `.gitignore` | Git 忽略規則 (保護敏感檔案) |

### 🛠️ 控制工具

| 檔案 | 說明 |
|------|------|
| `robot_control.sh` | Bash 控制腳本 |
| `robot_client.py` | Python API 客戶端 |

### 🗺️ 地圖視覺化

| 檔案 | 說明 |
|------|------|
| `map_visualizer.py` | 地圖視覺化 Python 腳本 |
| `map_output.png` | 產生的地圖圖片 |
| `map_dump.json` | 地圖原始資料 |

### 🔊 聲音與語音

| 檔案 | 說明 |
|------|------|
| `robot_sounds.md` | 聲音檔案分析與更換指南 |

### 🚀 MQTT 巡航控制

| 檔案 | 說明 |
|------|------|
| `mqttRover/rover_path_control.py` | 通用路徑控制 (支援方形/八邊形/圓形) |
| `mqttRover/rover_mqtt_square.py` | 方形巡航控制 |
| `mqttRover/rover_mqtt_octagon.py` | 八邊形巡航控制 |
| `mqttRover/clean_coords.py` | MQTT 座標監控工具 |
| `mqttRover/README.md` | MQTT 巡航使用說明 |

### 🔧 MiIO 協定工具

| 檔案 | 說明 |
|------|------|
| `miio_ping.py` | MiIO 基本 ping/指令工具 |
| `miio_ping_pro.py` | MiIO 診斷工具 (讀取歷史統計) |
| `debug_pos.py` | 嘗試讀取機器人座標 (實驗性) |

### 📦 資料傾印

| 檔案 | 說明 |
|------|------|
| `dump_data/` | 從機器人傾印的資料 |
| `blackbox/` | Blackbox 資料庫分析工具 |
| `dump_data/robot.db` | 清掃歷史資料庫 |
| `dump_data/rrlog/` | 系統日誌傾印 |

---

## 快速開始

### 安裝依賴

```bash
pip install paho-mqtt requests
```

### 連線到設備

```bash
# SSH (需先設定 ~/.ssh/config)
ssh robot

# 或直接 IP
ssh root@192.168.1.51
```

### 查詢狀態

```bash
# 方式 1: Bash 腳本
./robot_control.sh status

# 方式 2: 直接 curl
curl -s http://192.168.1.51/api/v2/robot/state/attributes

# 方式 3: Python
python3 -c "from robot_client import ValetudoClient; c = ValetudoClient(); c.print_info()"
```

### 控制命令

```bash
# 定位機器人
./robot_control.sh locate

# 開始清掃
./robot_control.sh start

# 返回充電座
./robot_control.sh home

# 設定風扇速度
./robot_control.sh fan max
```

### 執行巡航路徑

```bash
# MQTT Broker 需開啟並設定在 localhost
#方形巡航
python3 mqttRover/rover_path_control.py --shape square --size 80

# 八邊形巡航
python3 mqttRover/rover_path_control.py --shape octagon --size 100

# 圓形巡航 (16邊形)
python3 mqttRover/rover_path_control.py --shape circle --size 120
```

### 取得地圖

```bash
# 下載地圖 JSON
curl -s http://192.168.1.51/api/v2/robot/state/map -o map.json

# 視覺化
python3 map_visualizer.py map.json -o map.png
```

---

## 設備概要

| 項目 | 值 |
|------|-----|
| Model | Roborock V1 (rockrobo.vacuum.v1) |
| SoC | Allwinner A33 (ARM Cortex-A7 4-core) |
| GPU | ARM Mali-400 MP2 |
| Memory | 510 MB RAM |
| Storage | 3.8 GB eMMC |
| WiFi | Realtek RTL8188ES |
| Firmware | Valetudo 2026.02.0 |

### 主要埠口

| Port | Protocol | Service |
|------|----------|---------|
| 22 | TCP | SSH |
| 80 | TCP | Valetudo Web UI |
| 54321 | UDP | MiIO (內部) |
| 1883 | TCP | MQTT (需開啟) |

### Valetudo Web UI

- URL: http://192.168.1.51
- 使用者名稱: `valetudo`
- 密碼: (請見 `secrets.md`)

---

## 已知限制

- **無法完全關閉吸塵器**: 最低 PWM 0.01 (1%)
- **無法直接控制刷子馬達**: 只能透過風扇速度間接影響
- **無法讀取原始 LDS 數據**: 只能取得處理過的地圖
- **磁北方向無 API**: 只能讀取地圖相對角度
- **MiIO UDP 無法外部訪問**: 需 SSH 代理
- **MQTT 需啟用**: 巡航控制需要 Valetudo MQTT 功能開啟

---

## 隱私說明

**⚠️ 重要**: `secrets.md` 包含敏感資訊，已加入 `.gitignore`。

Valetudo 已阻斷所有到 Xiaomi 雲端的連線：
- 不上傳清掃地圖
- 不上傳 WiFi 設定
- 不上傳使用習慣資料
- 所有資料留在本地

---

## 延伸閱讀

- [Valetudo 文件](https://valetudo.cloud/)
- [XiaomiRobotVacuumProtocol](https://github.com/marcelrv/XiaomiRobotVacuumProtocol)
- [python-miio](https://python-miio.readthedocs.io/)
- [Valetudo RE](https://github.com/Hypfer/Valetudo)

---

*最後更新: 2026-04-17*
