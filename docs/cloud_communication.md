# Roborock V1 雲端通訊分析

**設備**: Roborock V1 (rockrobo.vacuum.v1)  
**最後更新**: 2026-04-16

---

## 1. 原本會傳送到 Xiaomi 伺服器的資料

> **注意**: 詳細敏感資料 (Token、金鑰等) 請見 `secrets.md`

### 1.1 設備識別資訊 (`miIO.info`)

| 欄位 | 說明 |
|------|------|
| `hw_ver` | 硬體版本 (如 "Linux") |
| `fw_ver` | 韌體版本 |
| `model` | 設備型號 (如 "rockrobo.vacuum.v1") |
| `mac` | 網卡 MAC 位址 |
| `token` | 認證 Token (16 bytes) |
| `did` | 設備 ID |
| `key` | 設備金鑰 |
| `life` | 運行分鐘數 |

### 1.2 WiFi 網路資訊

| 欄位 | 說明 |
|------|------|
| `ssid` | WiFi 名稱 |
| `bssid` | 路由器 MAC |
| `rssi` | 訊號強度 |
| `localIp` | 設備 IP |
| `uid` | 使用者 ID |

### 1.3 清掃歷史資料

| 欄位 | 說明 |
|------|------|
| `clean_time` | 總清掃時間 (秒) |
| `clean_area` | 總清掃面積 (cm²) |
| `clean_count` | 清掃次數 |

每次清掃記錄包含：開始/結束時間、持續時間、面積、錯誤碼、完成狀態

### 1.4 地圖資料

- **即時地圖**: RLE 編碼格式 (牆壁、地板、路徑)
- **歷史地圖**: 雲端 URL 格式

### 1.5 消耗品狀態

- main_brush_work_time (主刷)
- side_brush_work_time (邊刷)
- filter_work_time (濾網)
- sensor_dirty_time (感測器)

### 1.6 日誌上傳

- 目標: `cdn.cnbj0.files.fds.api.xiaomi.com`
- 用途: 故障診斷和遙測

---

## 2. Xiaomi 雲端伺服器清單

### 2.1 主要 API 伺服器

| 伺服器 | 地區 |
|--------|------|
| `ot.io.mi.com` | 中國 |
| `us.ot.io.mi.com` | 美國 |
| `eu.ot.io.mi.com` | 歐洲 |
| `sg.ot.io.mi.com` | 新加坡 |
| `tw.ot.io.mi.com` | 台灣 |

### 2.2 CDN/檔案伺服器

| 伺服器 |
|--------|
| `cdn.cnbj0.files.fds.api.xiaomi.com` |
| `awsbj0.fds.api.xiaomi.com` |
| `awssgp0.fds.api.xiaomi.com` |
| `awsde0.fds.api.xiaomi.com` |

### 2.3 Roborock 專用

| 伺服器 |
|--------|
| `iot.roborock.com` |

---

## 3. 通訊協定

### 3.1 MiIO UDP 協定

- **端口**: 54321 (UDP)
- **認證**: Token (XOR/MD5 加密)
- **格式**: JSON

### 3.2 HTTP API

- `POST /app/home/getmapfileurl` - 地圖下載
- `GET /v2/home/iot_gy_device` - 設備狀態

### 3.3 架構

```
機器人 (UDP:54321) → Xiaomi 雲端 → Mi Home App
```

---

## 4. Valetudo 的阻斷

Valetudo 透過 `/etc/hosts` 將雲端伺服器指向 `203.0.113.1`:

```bash
# 主要封鎖
203.0.113.1  ot.io.mi.com ott.io.mi.com
203.0.113.1  cdn.cnbj0.files.fds.api.xiaomi.com
203.0.113.1  iot.roborock.com
```

---

## 5. 隱私分析

### 原本會暴露的資料

| 資料類型 | 隱私風險 |
|----------|----------|
| WiFi SSID/密碼 | ⚠️ 高 |
| 清掃地圖 | 🔴 極高 |
| 清掃時間/習慣 | ⚠️ 中 |

### Valetudo 保護

- ✅ WiFi 留在本地
- ✅ 地圖不傳雲端
- ✅ 清掃歷史本地儲存
- ✅ 無遠端遙測

---

## 6. 資料來源

| 資料 | 來源 |
|------|------|
| 封鎖清單 | `ssh robot "cat /etc/hosts"` |
| 設備資訊 | `/mnt/data/miio/device.conf` |
| WiFi 設定 | `/mnt/data/wlan/wpa_supplicant.conf` |
| 清掃統計 | Valetudo API |
| 協定格式 | [XiaomiRobotVacuumProtocol](https://github.com/marcelrv/XiaomiRobotVacuumProtocol) |

---

*文件版本: 1.0*
