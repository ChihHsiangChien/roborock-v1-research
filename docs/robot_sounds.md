# Roborock V1 聲音檔案分析

**設備**: Roborock V1  
**最後更新**: 2026-04-16

---

## 1. 聲音檔案位置

### 目錄結構

```
/opt/rockrobo/resources/sounds/
├── power_on.wav              # 開機音效
├── start_greeting.wav        # 啟動問候語
├── tw/                       # 繁體中文 (目前使用)
├── prc/                      # 簡體中文
├── en/                       # 英文
├── Facsounds/               # 工廠測試音效
│   ├── prc/                 # 中文工廠測試
│   └── en/                  # 英文工廠測試
└── mtest/                   # 製造測試音效
```

### 各語言包大小

| 目錄 | 語言 | 檔案數 | 大小 |
|------|------|--------|------|
| `tw/` | 繁體中文 | 72 | 7.3 MB |
| `prc/` | 簡體中文 | 72 | 6.4 MB |
| `en/` | 英文 | 72 | 9.3 MB |
| `Facsounds/` | 工廠測試 | ~100 | 5.5 MB |
| `mtest/` | 製造測試 | ~60 | 2.2 MB |

---

## 2. 根目錄聲音檔

| 檔案 | 大小 | 用途 |
|------|------|------|
| `power_on.wav` | 670 KB | 開機音效 |
| `start_greeting.wav` | 84 KB | 啟動問候語 |

---

## 3. 台灣語音包 (繁體中文)

共 72 個 `.wav` 檔案，位於 `/opt/rockrobo/resources/sounds/tw/`

### 3.1 狀態提示

| 檔案 | 用途 |
|------|------|
| `start.wav` | 開始清掃 |
| `pause.wav` | 暫停 |
| `home.wav` | 返回充電座 |
| `finish.wav` | 清掃完成 |
| `clean_finish.wav` | 清掃完成 (另一版本) |
| `charging.wav` | 開始充電 |
| `spot.wav` | 定點清掃 |
| `zone.wav` | 區域清掃 |
| `remote.wav` | 遙控模式 |
| `remote_complete.wav` | 遙控完成 |
| `findme.wav` | 尋找機器人 (定位) |
| `wifi_reset.wav` | WiFi 重置 |

### 3.2 導航相關

| 檔案 | 用途 |
|------|------|
| `goto.wav` | 開始導航到定點 |
| `goto_complete.wav` | 定點導航完成 |
| `goto_failed.wav` | 定點導航失敗 |
| `stop_goto.wav` | 停止導航 |
| `back_dock_nearby.wav` | 接近充電座 |

### 3.3 清掃相關

| 檔案 | 用途 |
|------|------|
| `resume_clean.wav` | 恢復清掃 |
| `restart_clean.wav` | 重新開始清掃 |
| `resume_home.wav` | 恢復並返回 |
| `resume_zone.wav` | 恢復區域清掃 |
| `stop_spot.wav` | 停止定點清掃 |
| `stop_zone.wav` | 停止區域清掃 |
| `zone_complete.wav` | 區域清掃完成 |
| `zone_failed.wav` | 區域清掃失敗 |
| `timed_clean.wav` | 定時清掃 |
| `di.wav` | 清掃提示音 |

### 3.4 錯誤提示

| 檔案 | 用途 |
|------|------|
| `error1.wav` | 錯誤 1 |
| `error2.wav` | 錯誤 2 |
| `error3.wav` | 錯誤 3 |
| `error4.wav` | 錯誤 4 |
| `error5.wav` | 錯誤 5 |
| `error6.wav` | 錯誤 6 |
| `error7.wav` | 錯誤 7 |
| `error8.wav` | 錯誤 8 |
| `error9.wav` | 錯誤 9 |
| `error10.wav` | 錯誤 10 |
| `error11.wav` | 錯誤 11 |
| `error12.wav` | 錯誤 12 |
| `error13.wav` | 錯誤 13 |
| `error14.wav` | 錯誤 14 |
| `error15.wav` | 錯誤 15 |
| `error16.wav` | 錯誤 16 |
| `error17.wav` | 錯誤 17 |
| `error18.wav` | 錯誤 18 |
| `error19.wav` | 錯誤 19 |
| `error_internal.wav` | 內部錯誤 |
| `binout_error10.wav` | 塵盒錯誤 (錯誤 10) |

### 3.5 電源相關

| 檔案 | 用途 |
|------|------|
| `power_off.wav` | 關機 |
| `power_off_rejected.wav` | 拒絕關機 |
| `power_resume_clean.wav` | 恢復清掃 (電源) |
| `no_power.wav` | 電量不足 |
| `no_power_charging.wav` | 電量不足 (充電中) |
| `clean_bin.wav` | 清理塵盒提示 |

### 3.6 系統更新

| 檔案 | 用途 |
|------|------|
| `sysupd_start.wav` | 系統更新開始 |
| `sysupd_wip.wav` | 系統更新進行中 |
| `sysupd_complete.wav` | 系統更新完成 |
| `sysupd_failed.wav` | 系統更新失敗 |
| `sysupd_notready.wav` | 系統更新未就緒 |

### 3.7 Bootloader 復原

| 檔案 | 用途 |
|------|------|
| `bl_recovery_start.wav` | 復原開始 |
| `bl_recovery_retry.wav` | 復原重試 |
| `bl_recovery_failed.wav` | 復原失敗 |
| `bl_recovery_bootfailed.wav` | 開機失敗 |
| `bl_recovery_updatefailed.wav` | 更新失敗 |

### 3.8 對話回應

| 檔案 | 用途 |
|------|------|
| `return_yes.wav` | 是 (確認) |
| `return_no.wav` | 否 (取消) |

### 3.9 其他

| 檔案 | 用途 |
|------|------|
| `no_spot_on_dock.wav` | 找不到充電座 |
| `relocate_failed.wav` | 定位失敗 |

---

## 4. 工廠測試音效 (Facsounds)

位於 `/opt/rockrobo/resources/sounds/Facsounds/`

包含組裝測試時使用的音效，用於驗證各項硬體功能。

---

## 5. 製造測試音效 (mtest)

位於 `/opt/rockrobo/resources/sounds/mtest/`

包含製造過程中的測試音效。

---

## 6. 聲音格式規格

### WAV 檔案格式

```
檔案格式: RIFF (little-endian) data, WAVE audio
編碼方式: Microsoft PCM, 16 bit
取樣率:   16000 Hz (start_greeting.wav) 或 44100 Hz (其他)
聲道數:   Mono 或 Stereo
```

### 檔案權限

```
-rw-r--r-- root:root 644 (rw-r--r--)
```

---

## 7. 音訊硬體

### ALSA 音效設備

| 設備 | 說明 |
|------|------|
| 音效卡名稱 | audiocodec |
| PCM 播放設備 | `/dev/snd/pcmC0D0p` |
| PCM 錄音設備 | `/dev/snd/pcmC0D0c` |
| 控制設備 | `/dev/snd/controlC0` |

### 缺少的命令列工具

| 工具 | 用途 |
|------|------|
| `aplay` | 播放 WAV 檔案 |
| `amixer` | 控制音量 |

---

## 8. API 資訊

### VoicePackManagementCapability

```bash
# 取得語音包資訊
curl -s http://192.168.1.51/api/v2/robot/capabilities/VoicePackManagementCapability
```

回應:
```json
{
  "currentLanguage": "tw",
  "operationStatus": {
    "__class": "ValetudoVoicePackOperationStatus",
    "metaData": {},
    "type": "idle"
  }
}
```

---

## 9. 如何更換聲音檔

### 9.1 替換單一檔案

```bash
# 1. 從機器人下載原始檔案
scp robot:/opt/rockrobo/resources/sounds/tw/start.wav ./

# 2. 準備新的 WAV 檔案
# 格式要求: 16-bit PCM, 16000 Hz, Mono

# 3. 上傳新檔案到機器人
scp ./my_custom_start.wav robot:/opt/rockrobo/resources/sounds/tw/start.wav

# 4. 設定正確權限
ssh robot "chmod 644 /opt/rockrobo/resources/sounds/tw/start.wav"

# 5. 測試播放 (需找到播放方式)
```

### 9.2 替換整個語音包

```bash
# 1. 在本機建立新資料夾
mkdir -p my_voice_pack/tw

# 2. 複製所有 72 個 WAV 檔案到新資料夾

# 3. 上傳到機器人
scp -r ./my_voice_pack/tw robot:/opt/rockrobo/resources/sounds/tw/

# 4. 設定權限
ssh robot "chmod -R 644 /opt/rockrobo/resources/sounds/tw/"
```

### 9.3 自訂開機音效

```bash
# 開機音效位於
/opt/rockrobo/resources/sounds/power_on.wav

# 問候語位於
/opt/rockrobo/resources/sounds/start_greeting.wav

# 上傳自訂音效
scp ./my_power_on.wav robot:/opt/rockrobo/resources/sounds/power_on.wav
```

### 9.4 切換語言包

目前機器人使用 `tw` (繁體中文)。要切換到其他語言：

1. **方法 A**: 備份並複製
```bash
# 備份當前語音包
ssh robot "mv /opt/rockrobo/resources/sounds/tw /opt/rockrobo/resources/sounds/tw.bak"

# 複製其他語音包
ssh robot "cp -r /opt/rockrobo/resources/sounds/en /opt/rockrobo/resources/sounds/tw"
```

2. **方法 B**: 使用 Valetudo API (如有支援)

---

## 10. 聲音檔案大小分析

### 台灣語音包各檔案大小

| 檔案類型 | 預估大小 | 說明 |
|----------|----------|------|
| 錯誤提示 | 128-214 KB | 較長的語音說明 |
| 系統更新 | 100-200 KB | 中等長度 |
| 狀態提示 | 34-129 KB | 標準提示音 |
| 簡短提示 | ~34 KB | 快速提示 |

---

## 11. 備份建議

在修改聲音檔之前強烈建議備份：

```bash
# 備份整個 sounds 目錄
ssh robot "tar -czvf /mnt/data/sounds_backup.tar.gz /opt/rockrobo/resources/sounds/"

# 下載備份到本地
scp robot:/mnt/data/sounds_backup.tar.gz ./

# 或只備份當前語音包
scp -r robot:/opt/rockrobo/resources/sounds/tw ./tw_backup/
```

---

## 12. 注意事項

1. **韌體更新**: 可能會覆蓋 `/opt/rockrobo/resources/sounds/` 目錄
2. **資料夾結構**: 請保持 `tw/`, `prc/`, `en/` 資料夾結構
3. **檔案權限**: 上傳後需設定為 644
4. **WAV 格式**: 必須為 16-bit PCM 格式
5. **取樣率**: 建議使用 16000 Hz 或 44100 Hz

---

## 13. 資料來源

| 資料 | 來源 |
|------|------|
| 聲音檔位置 | `/opt/rockrobo/resources/sounds/` |
| 語音包設定 | Valetudo API VoicePackManagementCapability |
| 音效設備 | `/dev/snd/` |
| 備份位置 | `/mnt/data/` |

---

*文件版本: 1.0*
