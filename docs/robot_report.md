# Roborock V1 掃地機器人系統報告

**主機名稱**: rockrobo  
**IP 位址**: 192.168.1.51  

---

## 1. 基本資訊

### 作業系統
| 項目 | 值 |
|------|-----|
| OS | Ubuntu 14.04.3 LTS (Trusty Tahr) |
| 核心版本 | Linux 3.4.39 |
| 架構 | armv7l (32-bit ARM) |
| 編譯器 | gcc 4.8.2 |
| 主機名 | rockrobo |
| 時區 | Asia/Shanghai (CST-8) |

---

## 2. 硬體規格

### SoC (系統單晶片)
| 項目 | 值 |
|------|-----|
| 型號 | Allwinner A33 (sun8i) |
| 架構 | ARMv7 Cortex-A7 |
| 核心數 | 4 |
| BogoMIPS | 3085.71 |
| GPU | ARM Mali-400 MP2 (2 核心) |

### GPU (ARM Mali-400 MP2)

| 項目 | 值 |
|------|-----|
| 型號 | ARM Mali-400 MP2 |
| 核心數 | 2 |
| 設備節點 | `/dev/mali` (10:49) |
| 記憶體使用 | 208,075 KB (~203 MB) |
| 載入模組 | `mali`, `disp` |

**用途**:
- 顯示驅動 (`disp` 模組)
- SLAM 地圖處理的輔助計算
- 這是 Allwinner A33 SoC 的標準配備

### Cedar 影片引擎

| 項目 | 值 |
|------|-----|
| 型號 | Allwinner CedarX |
| 設備節點 | `/dev/cedar_dev` (150:0) |
| 中斷 | IRQ 90 (GIC) |
| 內核模組 | sunxi-cedar |

**功能**:
- H.264/H.265 影片解碼
- JPEG 編碼/解碼
- 影片後處理

**在掃地機器人上的用途** (推測):
- 地圖影像處理
- 語音提示音的音訊處理
- 備用功能（工廠測試或未來擴展）

**開機日誌**:
```
[    2.190358] sunxi cedar version 0.1 
[    2.194302] [cedar]: install start!!!
[    2.198494] [cedar]: install end!!!
```

### 多媒體硬體架構

```
Allwinner A33 SoC
├── CPU: ARM Cortex-A7 x4 @ 1.2 GHz
├── GPU: ARM Mali-400 MP2 ◄── 圖形處理
├── VPU: CedarX 影片引擎 ◄── 影片編解碼
└── ISP: 影像訊號處理器
```

### CPU
| 項目 | 值 |
|------|-----|
| 型號 | ARMv7 Processor rev 5 (v7l) |
| 核心數 | 4 |
| 架構 | ARMv7 |
| 速度 | 1.2 GHz (推估) |

### 記憶體
| 項目 | 值 |
|------|-----|
| 總記憶體 | 510,532 KB (~498 MB) |
| 已使用 | 363,532 KB (~355 MB) |
| 可用 | 147,000 KB (~144 MB) |
| Buffers | 22,164 KB |
| Cached | 119,232 KB |
| Swap | 無 |

### WiFi 晶片
| 項目 | 值 |
|------|-----|
| 型號 | Realtek RTL8188ES (RTL871X) |
| 模組 | 8189es (已載入) |
| MAC 位址 | 78:11:dc:e7:d5:28 |
| 訊號品質 | 94/100 |

### 儲存 (eMMC)
| 分區 | 大小 | 已用 | 可用 | 掛載點 | 用途 |
|------|------|------|------|--------|------|
| mmcblk0p1 | 1.6 GB | 190 MB | 1.3 GB | /mnt/data | 用戶資料 |
| mmcblk0p2 | 8 MB | - | - | boot-res | 開機資源 |
| mmcblk0p5 | 16 MB | - | - | env | 環境變數 |
| mmcblk0p6 | 16 MB | 1.2 MB | 14 MB | /mnt/default | 工廠設定 (唯讀) |
| mmcblk0p7 | 512 MB | - | - | recovery | 復原分區 |
| mmcblk0p8 | 512 MB | 264 MB | 205 MB | / (rootfs) | 系統 A |
| mmcblk0p9 | 512 MB | - | - | system_b | 系統 B (備份) |
| mmcblk0p10 | 528 MB | 263 MB | 206 MB | /mnt/updbuf | 下載/更新緩衝 |
| mmcblk0p11 | 16 MB | 2.1 MB | 13 MB | /mnt/reserve | 保留區 |
| mmcblk0boot0 | 2 MB | - | - | - | 開機分區 0 |
| mmcblk0boot1 | 2 MB | - | - | - | 開機分區 1 |

**總容量**: 3.8 GB eMMC

### 核心模組
```
8189es               1139096  0      # WiFi 網卡
g_android              37611  1      # Android 框架
mali                  208075  5      # GPU 驅動 (使用中)
ump                    40682  2      # 統一記憶體管理
disp                  991445  2 mali # 顯示控制器 (依賴 mali)
```

**模組關係**:
- `disp` → 依賴 `mali`
- `mali` → 依賴 `ump`
- 總 GPU 記憶體使用: ~203 MB

### 關鍵設備節點
| 設備 | 說明 |
|------|------|
| /dev/mmcblk0 | eMMC 區塊裝置 |
| /dev/ttyS0 | 主控台序列埠 |
| /dev/ttyS1 | LDS 雷射測距儀序列埠 |
| /dev/ttyS2 | MCU 通訊序列埠 |
| /dev/uart_lds | LDS UART |
| /dev/uart_mcu | MCU UART |
| /dev/cedar_dev | CedarX 影片編解碼引擎 (150:0) |
| /dev/disp | 顯示控制器 (250:0) |
| /dev/mali | Mali GPU (10:49) |
| /dev/leds | LED 控制 |
| /dev/lds_motor | LDS 馬達控制 |
| /dev/watchdog | 看門狗計時器 |

---

## 3. 網路設定

### 網路介面
| 介面 | 狀態 | IP 位址 | MAC 位址 |
|------|------|---------|----------|
| lo | UP | 127.0.0.1/8 | 00:00:00:00:00:00 |
| wlan0 | UP | 192.168.1.51/24 | 78:11:dc:e7:d5:28 |
| wlan1 | DOWN | - | 7a:11:dc:e7:d5:28 |

### 路由
- 預設閘道: 192.168.1.1 (via wlan0)
- 本地網段: 192.168.1.0/24

### DNS
- nameserver: 192.168.1.1
- domain: local

### WiFi 設定
- SSID: khjhcam
- 安全模式: WPA
- UID: 1337

### Valetudo hosts 設定
已封鎖以下 Xiaomi/Roborock 雲端服務:
- ot.io.mi.com, ott.io.mi.com (多地區)
- cdn.cnbj0.files.fds.api.xiaomi.com
- cnbj0.fds.api.xiaomi.com
- awsbj0.fds.api.xiaomi.com
- awssgp0.fds.api.xiaomi.com
- awsde0.fds.api.xiaomi.com
- iot.roborock.com

---

## 4. 軟體與服務

### 已安裝軟體版本

| 軟體 | 版本 |
|------|------|
| Valetudo | 2026.02.0 |
| Valetudo Commit | e4c924f1cf68da2753133677cbef42efb6ff0c3f |
| Valetudo System ID | GrubbyQualifiedPartridge |
| Node.js Runtime | v22.18.0-Valetudo |
| Rockrobo Version | 3.5.8_004018 |
| Build Number | 2020052901REL |
| Firmware Target | 1.12.0.0 |
| JavaScript Max Heap | 42 MiB |

### 運行中的服務 (Listening Ports)

| Port | Protocol | 服務 | 說明 |
|------|----------|------|------|
| 22 | TCP | sshd | SSH 遠端登入 |
| 80 | TCPv6 | valetudo | Web UI (HTTP) |
| 6665 | TCP | player | 清掃進程控制 |
| 5037 | TCP | adbd | ADB 守護進程 |
| 8079 | TCP | valetudo | Valetudo API |
| 54322 | TCP | miio_client | MIIO 客戶端 |
| 54323 | TCP | miio_client | MIIO 客戶端 |

### 主要行程

| PID | 名稱 | CPU% | MEM% | 說明 |
|-----|------|------|------|------|
| 820 | player | 6.3% | 19.2% | 清淨機器人主進程 |
| 21366 | valetudo | 1.0% | 9.9% | 開源韌體控制介面 |
| 761 | WatchDoge | 0.6% | 7.3% | 看門狗監控進程 |
| 797 | rrlogd | 0.7% | 0.5% | 日誌記錄進程 |
| 635 | haveged | 0.1% | 0.6% | 隨機數生成 |
| 4320 | sshd | 0.0% | 0.4% | SSH 伺服器 |
| 17894 | miio_client | 0.2% | 0.0% | Xiaomi MIIO 客戶端 |

---

## 5. 系統運行歷史

### 本次開機
- **開機時間**: 2026-04-16 15:36
- **運行時間**: 2小時55分鐘
- **開機原因**: 16 (電源重置)
- **負載**: 1.11-1.19

### 韌體版本歷史記錄

從 `/mnt/data/rockrobo/rrlog/` 中的日誌檔案可見:

| 紀錄編號 | 時間戳記 | 原始韌體版本 | 目前韌體版本 |
|----------|----------|--------------|--------------|
| 007021 | 20260416151033597 | 2017110300REL | - |
| 007022 | 20260416153241598 | 2017110300REL | - |
| 007023 | 20260416153313086 | 2017110300REL | 2020052901REL |
| 007024 | 20260416153604939 | 2017110300REL | 2020052901REL |


---

## 6. 清掃歷史資料庫

### 資料庫位置
`/mnt/data/rockrobo/robot.db`

### 資料表結構
- **cleanrecords**: 清掃記錄表
  - begin, daybegin, end, code, duration, area, error, complete
  
- **cleanmaps**: 地圖資料表
  - begin, daybegin, map (blob)
  
- **snapshot**: 快照表
  - id, duration, area, map (blob)

### 清掃統計設定
- **真空吸力 PWM**: 0.6 (60%)

---

## 7. 定時打擾 (DND) 設定

| 類型 | 時間 | 執行日期 |
|------|------|----------|
| DND 開始 | 22:00 - 08:00 | 週一至週日 |
| DND 結束 | 08:00 | - |

---

## 8. Valetudo 設定


### MQTT 設定
- **狀態**: 已停用

### Homie/HA 介面
- **Homie**: 已啟用
- **Home Assistant**: 已啟用

---

## 9. 設備驅動程式設定

### Chassis 驅動 (ruby_chassis)
| 參數 | 值 |
|------|-----|
| 最大速度 | 0.5 m/s |
| 最大偏航速度 | 3.14 rad/s |
| 機器人半徑 | 0.1725 m (17.25 cm) |
| 心跳超時 (MCU) | 10000 ms |
| 心跳周期 (MCU) | 1000 ms |
| 里程計輪徑 | 0.220 m (左右) |
| 編碼器頻率 | 256 Hz |

**感測器介面**:
- odo2d, gyro, odo, odo_gyro_for_slam (位置/里程)
- bumper, wall, sonar, cliff (障礙檢測)
- power, vaccuum, main, right (馬達控制)
- keypad, drop, dustin_status (狀態感測)

### Laser 驅動 (ruby_laser)
| 參數 | 值 |
|------|-----|
| 型號 | LDS (Laser Distance Sensor) |
| 介面 | raw:::laser:0, nav:::laser:1, slam:::laser:2 |
| 序列埠 | /dev/ttyS1 |
| 角度範圍 | -180° 到 180° |
| 最大範圍 | 6 m |
| 解析度 | 1° |
| 馬達轉速 | 270-330 RPM |
| 姿勢偏移 | [-0.100, 0.0, 0.0, 0.0, 0.0, 97.6] m/deg |

### LDS 感測器 (Ruby LDS)
| 項目 | 值 |
|------|-----|
| 位置 | x=-100mm, y=0, yaw=0° |
| 最小範圍 | 130 mm |
| 最大範圍 | 6000 mm |
| 有效強度閾值 | 200 |

### LDS 數據存取限制
| 方式 | 可用性 | 說明 |
|------|--------|------|
| Valetudo REST API | ❌ | 不提供原始掃描數據 |
| Valetudo 地圖 | ⚠️ | 只有處理過的地圖 (壓縮格式) |
| Player 框架 | ⚠️ | 需 SSH，端口 6665 被封鎖 |
| 直接串口讀取 | ❌ | /dev/ttyS1 需要特殊權限 |

**結論**: 原始 LDS 掃描數據無法直接讀取，只能取得處理過的地圖數據。

### Compass 驅動 (ruby_compass)
| 參數 | 值 |
|------|-----|
| 延遲 | 20 ms |
| 閾值 | 500 |
| 驅動名稱 | librubycompassdriver |

### SLAM 設定
| 參數 | 值 |
|------|-----|
| SLAM 類型 | rrSLAM (type 1) |
| 地圖大小 | 1024 像素 |
| 地圖比例 | 20 (1:20) |
| 粒子數 | 800 |
| GPU 加速 | 啟用 |

### 機器人移動參數
| 參數 | 值 |
|------|-----|
| 最小速度 | 0.05 m/s |
| 最大速度 | 0.3 m/s |
| 最小偏航速度 | -180 °/s |
| 最大偏航速度 | 180 °/s |
| 清掃半徑 | 50 mm |
| 機器人碰撞半徑 | 175 mm |

### 懸崖感測器 (Cliff)
| 感測器 | 位置角度 |
|--------|----------|
| 右前 (RF) | 4° |
| 左前 (LF) | -16.55° |
| 右 (R) | 16.55° |
| 左 (L) | -67.86° |

### 牆壁感測器
| 參數 | 值 |
|------|-----|
| 位置 | x=39.18mm, y=-160.21mm, yaw=-64° |

### 碰撞感測器 (Bumper)
| 參數 | 值 |
|------|-----|
| 碰撞器數量 | 3 |
| 半徑 | 0.1725 m |
| 碰撞角度 | 45°, 45°, 0° |

### 里程計 (Odometry)
| 參數 | 值 | 說明 |
|------|-----|------|
| 輪徑 | 0.220 m | 左右輪相同 |
| 編碼器頻率 | 256 Hz | 脈衝/秒 |
| Y偏移 | ±0.1195 m | 左右輪中心距 |
| 里程更新週期 | 50 ms | 速度更新間隔 |
| 失落閾值 | 250×20ms | 里程失效錯誤閾值 |

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/ruby_chassis.cfg`

### 馬達控制
| 馬達 | 介面 | 說明 |
|------|------|------|
| 左輪 | motor:1 | 由系統自動控制 |
| 右輪 | motor:2 | 由系統自動控制 |
| 真空吸塵 | vaccuum:::motor:0 | 可透過 API 調整 |
| 主刷 | main:::motor:1 | 自動根據風扇速度調整 |
| 邊刷 | right:::motor:2 | 自動根據風扇速度調整 |

### 主刷/邊刷 PWM 設定

| 馬達 | 正常模式 | 慢速模式 | 說明 |
|------|---------|---------|------|
| 主刷 (Main Brush) | 0.70 (70%) | 0.30 (30%) | 根據速度模式自動切換 |
| 邊刷 (Side Brush) | 0.85 (85%) | 0.35 (35%) | 根據速度模式自動切換 |

**控制限制**: 無法直接控制刷子馬達，只能透過調整風扇速度間接影響。

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/ruby_chassis.cfg`, `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg`

### 直線行走控制 (GoStraight)
| 參數 | 值 | 說明 |
|------|-----|------|
| 最小速度 | 0.1 m/s | 直線行走最低速 |
| 最大速度 | 0.3 m/s | 直線行走最高速 |
| 超越速度 | 0.15 m/s | 修正時速度 |
| 最大偏航速度 | 45 °/s | 方向修正最大角速度 |
| 行走直線距離閾值 | 20 mm | 觸發修正的偏差 |
| 啟動角度誤差 | 10° | 啟動時允許誤差 |

**直線控制流程**:
```
目標方向 → 里程計計算位移 → 陀螺儀檢測偏航角偏差 
→ 若偏差 > 20mm → 修正偏航速度 (最高 45°/s)
```

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg`

### 陀螺-里程融合 (Gyro-Odometry Fusion)
| 參數 | 值 | 說明 |
|------|-----|------|
| 偏差閾值比例 | 0.5 | 陀螺與里程偏差容許比例 |
| 偏差計數上限 | 42 | 最大連續偏差計數 |
| 高閾值 | 40 | 觸發警告 |
| 低閾值 | 30 | 恢復正常 |
| 里程更新 (odo) | 256 Hz | 里程計頻率 |

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg`

### 吸塵器馬達
| 參數 | 值 |
|------|-----|
| 介面 | vaccuum:::motor:0 |
| 驅動程式 | libchassisdriver.so |
| 預設 PWM | 0.6 (60%) |
| 設定檔案 | /mnt/data/rockrobo/VacuumAndBrush.cfg |

**不同模式的風扇 PWM**:

| 模式 | PWM 值 | 說明 |
|------|--------|------|
| 正常清掃 | 0.60 | 60% |
| 回充模式 | 0.30 | 30% |
| 定點清掃 | 0.70 | 70% |
| 最低速 (min) | 0.01 | 1% |

**吸塵器控制限制**:
- Valetudo FanSpeedControlCapability 提供 5 種速度：min, low, medium, high, max
- **無法完全關閉吸塵器** - 無 "off" 選項
- 最低速為 `min` (PWM 0.01，約 1% 功率)
- 回充時 (docked) 風扇降至 0.30 (30%)，非完全關閉
- 馬達在機器人啟動時自動運行

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (VACUUM_PWM_*), `/mnt/data/rockrobo/VacuumAndBrush.cfg` (當前設定)

### 方位感測器
| 感測器 | 介面 | 驅動程式 |
|--------|------|----------|
| 電子羅盤 | compass:::position3d:2 | librubycompassdriver.so |
| 陀螺儀 | gyro:::position3d:0 | 整合於 chassis |
| 里程+陀螺融合 | odo_gyro_for_slam:::position3d:1 | SLAM 用 |

### 方位角類型

**重要區分**：

| 角度來源 | 類型 | 可讀取 | 說明 |
|----------|------|--------|------|
| Valetudo 地圖 API | 地圖相對座標 | ✅ | 相對於地圖建立時的原點 |
| 電子羅盤 (磁北) | 地磁方位角 | ❌ | 無 API |

**地圖 API 回傳的 90 度角是相對於地圖座標系，不是磁北方向。**

### 電子羅盤設定

| 參數 | 值 |
|------|-----|
| 驅動程式 | librubycompassdriver.so |
| 軸數 | 3 軸 (X, Y, Z) |
| 校準狀態 | HAS_CALIBRATED 0 (未校準) |
| 羅盤閾值 | 2000 |
| 校準閾值 | 1100 |
| 弱信號閾值 | 700 |

**電子羅盤用途**：
- 困住偵測 (Trap Detection)
- 羅盤碰撞保護
- 導航修正

### 方位角相關參數

| 參數 | 值 |
|------|-----|
| 最大偏航速度 | 3.14 rad/s |
| 安全旋轉角度 | 35° |
| 轉向速度 | 45-90 °/s |
| 左轉角度 | 90° |
| 右轉角度 | 180° |
| 旋轉速度 | 45 °/s |

### 方位角控制限制

| 功能 | 可用性 |
|------|--------|
| 讀取方位角 (地圖座標) | ✅ |
| 讀取磁北方位角 | ❌ |
| 設定目標朝向 | ❌ |
| 旋轉到特定角度 | ❌ |
| HighResolutionManualControl | ❌ (已停用) |

**資料來源**: `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg`
| LDS 姿勢偏移 | x=-100mm, yaw=97.6° |

---

## 10. 核心與開機資訊

### 核心版本
```
Linux version 3.4.39 
(gcc version 4.8.2 (Ubuntu/Linaro 4.8.2-16ubuntu4))
SMP PREEMPT
```

### 開機命令列
```
rootwait boot_fs=a console=ttyS0,115200 root=/dev/mmcblk0p8 
rootfstype=ext4 loglevel=7 
partitions=boot-res@mmcblk0p2:env@mmcblk0p5:app@mmcblk0p6:
          recovery@mmcblk0p7:system_a@mmcblk0p8:system_b@mmcblk0p9:
          Download@mmcblk0p10:reserve@mmcblk0p11:UDISK@mmcblk0p1 
boot_reason=0x75706764 location=tw boot_ver=2011.09-rc1-00008-g7ceab3e-dirty
```

### 開機分區配置
| 分區標籤 | 設備 | 用途 |
|----------|------|------|
| boot-res | mmcblk0p2 | 開機資源 |
| env | mmcblk0p5 | 環境變數 |
| app | mmcblk0p6 | 工廠應用程式 (唯讀) |
| recovery | mmcblk0p7 | 復原系統 |
| system_a | mmcblk0p8 | 當前運行系統 |
| system_b | mmcblk0p9 | 備份系統 |
| Download | mmcblk0p10 | 下載/更新緩衝 |
| reserve | mmcblk0p11 | 保留區 |
| UDISK | mmcblk0p1 | 用戶資料區 |

### 韌體建構資訊
| 項目 | 值 |
|------|-----|
| 建構日期 | 2026-04-15T07:40:09Z |
| 建構序號 | 4018 |
| 建構者 | dustbuilder (dontvacuum.me) |
| 核心日期 | 2020-05-29 19:10:05 CST |
| 開發板 | HP Z230 SFF Workstation |

### 工廠設定分區 (/mnt/default)
| 檔案 | 大小 | 內容 |
|------|------|------|
| device.conf | 97 bytes | 設備 ID、金鑰、MAC |
| librrafm.so | 22 KB | RF 射頻函式庫 |
| adb.conf | 12 bytes | ADB 鎖定設定 |
| vinda | 16 bytes | 品牌識別 |

### 更新套件資訊
```
版本: 1.12.0.0
MD5: d254538e9fe4f2796aa25aa022457e7e
URL: http://192.168.8.126:38757/firmware
下載狀態: NotStart
下載模式: Foreground
```

---

## 11. 最近系統事件

### Valetudo 日誌警告
大量 "Failed to parse uploaded map" 警告，可能表示:
- 地圖上傳功能存在問題
- 地圖資料格式不相容

### Miio 客戶端日誌
```
[2026-04-16 15:40:26] [ERROR] tz is not a string
timezone does not exist:/usr/share/zoneinfo/
[2026-04-16 15:40:41] [ERROR] miio_util.c,general_send_one: 17 send error: Broken pipe
```

### WiFi 連線重試
系統重試 2 次 WiFi 連線後成功連接

---

## 12. 安全性注意

- Valetudo 使用預設密碼 `abc12345`
- SSH 服務已啟用且可遠端存取
- 雲端服務已被 Valetudo hosts 檔案封鎖
- 設備已安裝開源 Valetudo 韌體替代原廠雲端控制

---

## 13. 目錄結構

```
/
├── /root/              # root 用戶家目錄
├── /opt/rockrobo/     # 掃地機器人應用程式
│   ├── cleaner/       # 清掃相關程式
│   ├── watchdog/      # 看門狗監控
│   ├── miio/          # 小米 MIIO 客戶端
│   ├── rrlog/         # 日誌工具
│   ├── resources/     # 資源檔案 (聲音等)
│   ├── scripts/       # 初始化腳本
│   └── wlan/          # WiFi 設定
├── /mnt/data/         # 資料儲存分區 (持久化)
│   ├── rockrobo/      # 機器人資料庫和設定
│   ├── miio/          # MIIO 設定
│   └── wlan/          # WiFi 設定
├── /mnt/default/      # 預設設定分區 (唯讀)
├── /mnt/updbuf/       # 韌體更新緩衝區
└── /mnt/reserve/      # 保留分區
```

---

## 14. 資料來源

本報告中所有資訊均透過 SSH 讀取機器人檔案取得，以下是各項資料的來源檔案與指令：

### 14.1 設備識別資料

| 資料 | 來源檔案 |
|------|----------|
| 設備 ID、金鑰、MAC | `/mnt/data/miio/device.conf` |
| 工廠設備資訊 | `/mnt/default/device.conf` |
| Token | `/mnt/data/miio/device.token` |

### 14.2 作業系統與核心

| 資料 | 來源檔案/指令 |
|------|--------------|
| OS 版本、核心版本 | `cat /etc/lsb-release` |
| 核心版本詳細資訊 | `cat /proc/version` |
| 核心命令列參數 | `cat /proc/cmdline` |
| 時區設定 | `cat /mnt/data/rockrobo/timezone` |

### 14.3 CPU 與記憶體

| 資料 | 來源檔案/指令 |
|------|--------------|
| CPU 型號、架構 | `cat /proc/cpuinfo` |
| 記憶體使用量 | `cat /proc/meminfo` |
| SoC 型號 (Hardware) | `cat /proc/cpuinfo` 中的 Hardware 欄位 |
| BogoMIPS | `cat /proc/cpuinfo` |

### 14.4 儲存與分區

| 資料 | 來源檔案/指令 |
|------|--------------|
| 分區表 | `cat /proc/partitions` |
| 掛載狀態 | `df -h` |
| 掛載資訊 | `cat /proc/mounts` |
| 分區標籤對應 | `/proc/cmdline` 中的 partitions 參數 |
| MBR 開機磁區 | `dd if=/dev/mmcblk0 bs=512 count=1` |

### 14.5 WiFi 與網路

| 資料 | 來源檔案/指令 |
|------|--------------|
| WiFi 晶片型號 | `lsmod` (8189es 模組) |
| WiFi 驅動日誌 | `dmesg` 中的 RTL871X 訊息 |
| 網路介面 MAC | `ip addr` 或 `cat /sys/class/net/wlan0/address` |
| WiFi 訊號品質 | `cat /proc/net/wireless` |
| WiFi 設定 | `/mnt/data/wlan/wifi.conf` |
| WiFi UID | `/mnt/data/miio/device.uid` |
| Valetudo hosts 封鎖 | `/etc/hosts` |

### 14.6 核心模組與設備節點

| 資料 | 來源檔案/指令 |
|------|--------------|
| 已載入模組 | `lsmod` |
| 區塊設備 | `cat /proc/devices` |
| 字元設備 | `ls -la /dev/` |
| GPU 裝置 | `/dev/mali`, `/dev/disp` |
| 影片引擎 | `/dev/cedar_dev` |
| 序列埠 | `/dev/ttyS0`, `/dev/ttyS1`, `/dev/ttyS2` |
| 中斷資訊 | `cat /proc/interrupts` |
| 開機日誌 | `dmesg` (sunxi cedar, mali) |

### 14.7 韌體與軟體版本

| 資料 | 來源檔案/指令 |
|------|--------------|
| Valetudo 版本 | Valetudo API `/api/v2` |
| Valetudo 設定 | `/mnt/data/valetudo_config.json` |
| 建構資訊 | `/mnt/updbuf/build.txt` |
| 韌體版本 | Valetudo API 或 `cat /opt/rockrobo/version` |
| 更新套件資訊 | `/mnt/data/rockrobo/Update.pkg.inf` |
| 開機原因 | `/mnt/data/rockrobo/rrlog/boot_reason` |
| 韌體歷史 | `/mnt/data/rockrobo/rrlog/` 目錄中的日誌檔 |

### 14.8 驅動程式設定

| 資料 | 來源檔案 |
|------|----------|
| Chassis 驅動設定 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/ruby_chassis.cfg` |
| Laser 驅動設定 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/ruby_chassis.cfg` |
| SLAM 設定 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/ruby_chassis.cfg` |
| LDS 感測器設定 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` |
| 導航/移動參數 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` |
| 懸崖/牆壁感測器 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` |
| 碰撞感測器參數 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` |
| 充電座設定 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/chargerIntensity.cfg` |
| 里程計/馬達設定 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/ruby_chassis.cfg` |
| 直線行走設定 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (GoStraight, StraightWalker) |
| 陀螺-里程融合 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (GYRO_ODO_*) |
| 吸塵器 PWM | `/mnt/data/rockrobo/VacuumAndBrush.cfg` (當前設定) |
| 吸塵器 PWM 模式 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (VACUUM_PWM_*) |
| 刷子馬達 PWM | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (MAIN_BRUSH_*, RIGHT_BRUSH_*) |
| GoTo 參數 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (GoTo, GoToOpenSpace) |
| 旋轉參數 | `/mnt/updbuf/opt/rockrobo/cleaner/conf/Nav.cfg` (ROTATION_*, YAW_SPEED) |

### 14.9 系統日誌

| 資料 | 來源檔案 |
|------|----------|
| Miio 客戶端日誌 | `/mnt/data/rockrobo/rrlog/miio.log` |
| 系統日誌 | `/mnt/data/rockrobo/rrlog/rrlog.log` |
| 看門狗日誌 | `/mnt/data/rockrobo/rrlog/watchdog.log` |
| 歷史韌體日誌 | `/mnt/data/rockrobo/rrlog/*.log.gz` |

### 14.10 清掃資料庫

| 資料 | 來源檔案 |
|------|----------|
| 清掃記錄 | `/mnt/data/rockrobo/robot.db` (SQLite) |
| - cleanrecords 表 | 清掃歷史記錄 |
| - cleanmaps 表 | 地圖資料 |
| - snapshot 表 | 快照資料 |

### 14.11 工廠預設分區

| 資料 | 來源檔案 |
|------|----------|
| 工廠設定 | `/mnt/default/device.conf` |
| 工廠 ADB 設定 | `/mnt/default/adb.conf` |
| 工廠韌體識別 | `/mnt/default/vinda` |

### 14.12 Valetudo API

| 資料 | 來源端點 |
|------|----------|
| 設備狀態 | `GET /api/v2/robot/state` |
| 地圖資料 (含方位角) | `GET /api/v2/robot/state/map` |
| 消耗品狀態 | `GET /api/v2/robot/capabilities/ConsumableMonitoringCapability` |
| 統計資料 | `GET /api/v2/robot/capabilities/TotalStatisticsCapability` |
| WiFi 設定 | `GET /api/v2/robot/capabilities/WifiConfigurationCapability` |
| 風扇預設值 | `GET /api/v2/robot/capabilities/FanSpeedControlCapability/presets` |
| GoTo 定點移動 | `PUT /api/v2/robot/capabilities/GoToLocationCapability` |
| 區域清掃 | `PUT /api/v2/robot/capabilities/ZoneCleaningCapability` |
| 方位角控制 | ❌ 無 API (HighResolutionManualControlCapability 已停用) |

---

*此報告由系統自動掃描生成*
