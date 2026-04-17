# Roborock V1 機器人研究文件

**設備**: Roborock V1 (rockrobo.vacuum.v1)  
**韌體**: Valetudo 2026.02.0 + 原廠 3.5.8_004018

---

## 📁 專案結構

```
roborock-v1-research/
├── README.md              # 本文件 (索引)
├── docs/                 # 詳細技術文件
├── scripts/              # 程式碼腳本
├── outputs/              # 輸出結果 (gitignored)
└── secrets.md            # 敏感資訊 (gitignored)
```

---

## 📚 技術文件 (docs/)

| 檔案 | 說明 |
|------|------|
| `robot_report.md` | 系統硬體/軟體詳細報告 |
| `robot_api.md` | Valetudo REST API 技術文件 |
| `robot_sounds.md` | 聲音檔案分析與更換指南 |
| `cloud_communication.md` | 雲端通訊與隱私分析 |

---

## 🛠️ 腳本工具 (scripts/)

| 目錄 | 說明 |
|------|------|
| `scripts/control/` | Bash 機器人控制腳本 |
| `scripts/api/` | Python API 客戶端 |
| `scripts/mqtt/` | MQTT 巡航控制工具 |
| `scripts/miio/` | MiIO 協定工具 |
| `scripts/visualization/` | 地圖視覺化工具 (Python + R) |

詳細說明見各目錄下的 README 或 `docs/` 中的技術文件。

---

## 🚀 快速開始

### 安裝依賴

```bash
pip install paho-mqtt requests
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
./scripts/control/robot_control.sh fan max  # 最大風扇
```

### 巡航控制 (需 MQTT)

```bash
python3 scripts/mqtt/rover_path_control.py --shape square --size 80
```

### 地圖視覺化

```bash
curl -s http://192.168.1.51/api/v2/robot/state/map -o map_dump.json
python3 scripts/visualization/map_visualizer.py map_dump.json -o outputs/map.png
```

---

## 設備概要

| 項目 | 值 |
|------|-----|
| Model | Roborock V1 |
| Firmware | Valetudo 2026.02.0 |
| SSH | port 22 |
| Web UI | port 80 (http://192.168.1.51) |

詳細規格見 `docs/robot_report.md`

---

## ⚠️ 敏感資料

`secrets.md` 包含設備密碼和認證金鑰，已加入 `.gitignore`。

---

*最後更新: 2026-04-17*
