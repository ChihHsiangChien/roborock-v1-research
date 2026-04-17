# Roborock V1 機器人研究文件

**設備**: Roborock V1 (rockrobo.vacuum.v1)  
**IP**: 192.168.1.51  
**韌體**: Valetudo 2026.02.0 + 原廠 3.5.8_004018

---

## 📁 專案結構

```
roborock-v1-research/
├── README.md              # 本文件
├── docs/                 # 文件目錄
│   ├── robot_report.md   # 系統硬體/軟體報告
│   ├── robot_api.md      # Valetudo REST API 技術文件
│   ├── robot_sounds.md   # 聲音檔案分析與更換指南
│   └── cloud_communication.md  # 雲端通訊分析
├── scripts/              # 腳本工具目錄
│   ├── control/          # 機器人控制腳本
│   ├── api/              # API 客戶端
│   ├── mqtt/             # MQTT 巡航控制
│   ├── miio/             # MiIO 協定工具
│   └── visualization/     # 地圖視覺化工具
├── outputs/              # 輸出結果 (圖片、動畫)
├── secrets.md            # 敏感資訊 ⚠️
└── .gitignore
```

---

## 📋 各目錄說明

### 🛠️ scripts/control/ - 機器人控制腳本

| 檔案 | 說明 |
|------|------|
| `robot_control.sh` | 主要控制腳本 (清掃、回充、定位等) |
| `test_robot_api.sh` | API 測試腳本 |

```bash
./scripts/control/robot_control.sh status    # 查看狀態
./scripts/control/robot_control.sh start     # 開始清掃
./scripts/control/robot_control.sh home      # 返回充電座
```

### 🌐 scripts/api/ - API 客戶端

| 檔案 | 說明 |
|------|------|
| `robot_client.py` | Python Valetudo API 客戶端 |
| `test_api.py` | API 測試腳本 |

```bash
python3 scripts/api/robot_client.py status
```

### 🚀 scripts/mqtt/ - MQTT 巡航控制

| 檔案 | 說明 |
|------|------|
| `rover_path_control.py` | 通用路徑控制 (方形/八邊形/圓形) |
| `rover_mqtt_square.py` | 方形巡航控制 |
| `rover_mqtt_octagon.py` | 八邊形巡航控制 |
| `clean_coords.py` | MQTT 座標監控工具 |
| `README.md` | 使用說明 |

```bash
# 需要先安裝依賴
pip install paho-mqtt requests

# 執行巡航
python3 scripts/mqtt/rover_path_control.py --shape square --size 80
```

### 🔧 scripts/miio/ - MiIO 協定工具

| 檔案 | 說明 |
|------|------|
| `miio_ping.py` | MiIO 基本 ping/指令工具 |
| `miio_ping_pro.py` | MiIO 診斷工具 (讀取歷史統計) |
| `debug_pos.py` | 嘗試讀取機器人座標 (實驗性) |

```bash
python3 scripts/miio/miio_ping.py
```

### 🗺️ scripts/visualization/ - 地圖視覺化工具

| 目錄/檔案 | 說明 |
|------|------|
| `map_visualizer.py` | Python 地圖視覺化工具 |
| `robot-map-analysis/` | R 語言地圖分析工具 |

#### Python 版本
```bash
curl -s http://192.168.1.51/api/v2/robot/state/map -o map_dump.json
python3 scripts/visualization/map_visualizer.py map_dump.json -o outputs/map.png
```

#### R 版本
```bash
cd scripts/visualization/robot-map-analysis
Rscript reconstruct_map.R
```

R 分析輸出:
- `spatial_map.png` - 空間地圖
- `efficiency.png` - 清掃效率
- `vitals.png` - 電池狀態
- `animation.gif` - 路徑動畫

---

## 📚 文件 (docs/)

| 檔案 | 說明 |
|------|------|
| `robot_report.md` | 完整系統硬體/軟體報告 |
| `robot_api.md` | Valetudo REST API 技術文件 |
| `robot_sounds.md` | 聲音檔案分析與更換指南 |
| `cloud_communication.md` | 原本傳送到 Xiaomi 雲端的資料分析 |

---

## 快速開始

### 安裝依賴

```bash
# Python 依賴
pip install paho-mqtt requests

# R 語言依賴 (用於地圖分析)
Rscript -e 'install.packages(c("jsonlite", "ggplot2", "dplyr", "tidyr", "gganimate", "showtext", "gifski"))'
```

### 連線到設備

```bash
ssh robot
# 或
ssh root@192.168.1.51
```

### 基本操作

```bash
# 查看狀態
./scripts/control/robot_control.sh status

# 控制機器人
./scripts/control/robot_control.sh locate    # 定位
./scripts/control/robot_control.sh start    # 開始清掃
./scripts/control/robot_control.sh home     # 返回充電座
./scripts/control/robot_control.sh fan max   # 最大風扇
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
