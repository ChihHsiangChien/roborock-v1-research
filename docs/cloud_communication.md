# Roborock V1 雲端通訊記錄

**設備**: Roborock V1 (rockrobo.vacuum.v1)  
**最後更新**: 2026-04-16

---

## 1. 原本會傳送到 Xiaomi 伺服器的資料

### 1.1 設備識別資訊 (`miIO.info`)

當設備連接到 Xiaomi 雲端時，會定期發送以下資訊：

| 欄位 | 說明 | 範例值 |
|------|------|--------|
| `hw_ver` | 硬體版本 | "Linux" |
| `fw_ver` | 韌體版本 | "3.5.8_004018" |
| `model` | 設備型號 | "rockrobo.vacuum.v1" |
| `mac` | 網卡 MAC 位址 | "78:11:DC:E7:D5:28" |
| `token` | 認證 Token (16 bytes) | "aFym5l1XUcKQMav5" |
| `did` | 設備 ID | 82512493 |
| `key` | 設備金鑰 | "xSTsRgev55Jtebag" |
| `life` | 運行分鐘數 | 62848 |

### 1.2 WiFi 網路資訊

| 欄位 | 說明 | 範例值 |
|------|------|--------|
| `ssid` | WiFi 名稱 | "khjhcam" |
| `bssid` | 路由器 MAC | (路由器位址) |
| `rssi` | 訊號強度 | -63 dBm |
| `localIp` | 設備 IP | 192.168.1.51 |
| `mask` | 子網路遮罩 | 255.255.255.0 |
| `gw` | 預設閘道 | 192.168.1.1 |
| `uid` | 使用者 ID | 1337 |

### 1.3 清掃歷史資料

#### 總結 (`get_clean_summary`)

| 欄位 | 說明 | 範例值 |
|------|------|--------|
| `clean_time` | 總清掃時間 (秒) | 1977128 (≈549 小時) |
| `clean_area` | 總清掃面積 (cm²) | 312690000 (≈312.69 m²) |
| `clean_count` | 清掃次數 | 1417 |

#### 詳細記錄 (`get_clean_record`)

每次清掃記錄包含：
- 開始時間 (Unix timestamp)
- 結束時間 (Unix timestamp)
- 持續時間 (秒)
- 清掃面積 (cm²)
- 錯誤碼
- 完成狀態 (0=未完成, 1=完成)

### 1.4 地圖資料

#### 即時地圖 (`get_map`, `get_map_v1`)

- RLE 編碼格式的地圖數據
- 包含牆壁、地板、路徑資訊
- 機器人位置和朝向

#### 歷史地圖 (`get_clean_record_map`)

- 返回雲端地圖 URL
- 格式: `roboroommap%22[did]%2F[序號]`
- 下載位置: `https://[country].api.io.mi.com/app/home/getmapfileurl`

### 1.5 消耗品狀態 (`get_consumable`)

| 消耗品 | 說明 |
|--------|------|
| main_brush_work_time | 主刷使用時間 (秒) |
| side_brush_work_time | 邊刷使用時間 (秒) |
| filter_work_time | 濾網使用時間 (秒) |
| sensor_dirty_time | 感測器清潔計時 (秒) |

### 1.6 日誌上傳 (`enable_log_upload`)

| 欄位 | 說明 |
|------|------|
| `log_upload_status` | 日誌上傳狀態 |
| 目標伺服器 | `cdn.cnbj0.files.fds.api.xiaomi.com` |
| 目的 | 故障診斷和遙測 |

---

## 2. Xiaomi 雲端伺服器清單

### 2.1 主要 API 伺服器

| 伺服器 | 地區 | 用途 |
|--------|------|------|
| `ot.io.mi.com` | 中國 | 主要 API 端點 |
| `us.ot.io.mi.com` | 美國 | 美國區域 |
| `eu.ot.io.mi.com` | 歐洲 | 歐洲區域 |
| `sg.ot.io.mi.com` | 新加坡 | 東南亞區域 |
| `tw.ot.io.mi.com` | 台灣 | 台灣區域 |

### 2.2 OTA 更新伺服器

| 伺服器 | 用途 |
|--------|------|
| `ott.io.mi.com` | 韌體 OTA 更新 |
| 各地區變體 | 各地區專用 |

### 2.3 CDN/檔案伺服器

| 伺服器 | 用途 |
|--------|------|
| `cdn.cnbj0.files.fds.api.xiaomi.com` | CDN 北京 |
| `awsbj0.fds.api.xiaomi.com` | AWS 北京 |
| `awssgp0.fds.api.xiaomi.com` | AWS 新加坡 |
| `awsde0.fds.api.xiaomi.com` | AWS 德國 |
| `awsusor0.fds.api.xiaomi.com` | AWS 美國 |

### 2.4 Roborock 專用

| 伺服器 | 用途 |
|--------|------|
| `iot.roborock.com` | Roborock 雲端服務 |

---

## 3. 通訊協定

### 3.1 MiIO UDP 協定

**端口**: 54321 (UDP)

**特性**:
- 設備發起連線到雲端伺服器
- 使用 XOR 加密 + Token 認證
- JSON 格式訊息

**封包結構**:
```
[Length:4][Token:16][Random:4][[Payload][Checksum:4]
```

### 3.2 HTTP API

**認證**: OAuth 2.0 + Device Token

**主要端點**:
- `POST /app/home/getmapfileurl` - 取得地圖下載 URL
- `GET /v2/home/iot_gy_device` - 設備狀態
- `POST /v2/home/device` - 設備控制

### 3.3 實體連線架構

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   機器人     │  UDP    │   Xiaomi     │  HTTP   │  Mi Home    │
│   (Port     │ ──────► │   雲端       │ ──────► │   App       │
│   54321)    │         │   伺服器     │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
```

---

## 4. Valetudo 的阻斷措施

Valetudo 透過 `/etc/hosts` 將所有 Xiaomi 伺服器指向廢棄 IP `203.0.113.1`:

```bash
# /etc/hosts (Valetudo 追加)
203.0.113.1  ot.io.mi.com ott.io.mi.com
203.0.113.1  cdn.cnbj0.files.fds.api.xiaomi.com
203.0.113.1  iot.roborock.com
# ... 其他伺服器
```

**效果**:
- 設備無法連接真正的雲端伺服器
- 所有功能在本地處理
- 不上傳任何資料到網路

---

## 5. 隱私分析

### 5.1 原本會暴露的資料

| 資料類型 | 隱私風險 | 說明 |
|----------|----------|------|
| WiFi SSID/密碼 | ⚠️ 高 | 家庭網路名稱 |
| MAC 位址 | ⚠️ 中 | 設備唯一識別 |
| IP 位址 | ⚠️ 中 | 網路位置 |
| 清掃地圖 | 🔴 極高 | 住宅平面圖 |
| 清掃時間 | ⚠️ 中 | 在家時間習慣 |
| 使用習慣 | ⚠️ 中 | 生活作息分析 |

### 5.2 Valetudo 保護的隱私

- ✅ WiFi 設定留在本地
- ✅ 地圖資料不傳送到雲端
- ✅ 清掃歷史本地儲存
- ✅ 無遠端遙測
- ✅ 可離線運作

---

## 6. 資料來源

本文件的資料來源：

| 資料 | 來源 |
|------|------|
| 封鎖的伺服器清單 | `ssh robot "cat /etc/hosts"` |
| 設備識別 | `/mnt/data/miio/device.conf` |
| WiFi 設定 | `/mnt/data/wlan/wifi.conf` |
| 清掃統計 | Valetudo API `/api/v2/robot/capabilities/TotalStatisticsCapability` |
| MiIO 協定格式 | [XiaomiRobotVacuumProtocol](https://github.com/marcelrv/XiaomiRobotVacuumProtocol) |

---

*文件版本: 1.0*
