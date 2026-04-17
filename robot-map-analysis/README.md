# Roborock 地圖分析工具 (R 語言)

使用 R 語言分析 Valetudo 掃地機器人的清掃地圖資料，生成視覺化報告。

## 📁 檔案說明

| 檔案 | 說明 |
|------|------|
| `reconstruct_map.R` | **主程式** - 生成空間地圖、效率分析、電池狀態和動畫 |
| `inspect_map.R` | 快速檢視地圖結構 (layers, entities, attributes) |
| `inspect_data.R` | 詳細檢視地圖屬性和路徑資料 |
| `inspect_time.R` | 檢視時間序列和統計資料 |
| `check_states.R` | 檢查清掃開始/結束時的狀態 |

### 輸出檔案

| 檔案 | 說明 |
|------|------|
| `spatial_map.png` | 空間地圖 (含清掃路徑) |
| `efficiency.png` | 清掃效率趨勢圖 |
| `vitals.png` | 電池電量變化圖 |
| `animation.gif` | 路徑動畫 (GIF) |

## 🔧 安裝依賴

```r
# 在 R 中執行
install.packages(c("jsonlite", "ggplot2", "dplyr", "tidyr", "gganimate", "showtext", "gifski"))
```

或使用終端機：
```bash
Rscript -e 'install.packages(c("jsonlite", "ggplot2", "dplyr", "tidyr", "gganimate", "showtext", "gifski"))'
```

## 🚀 使用方式

### 1. 準備地圖資料

從機器人下載地圖 JSON：
```bash
curl -s http://192.168.1.51/api/v2/robot/state/map -o map_dump.json
```

### 2. 執行分析

```bash
# 在 robot-map-analysis 目錄中執行
cd robot-map-analysis
Rscript reconstruct_map.R
```

### 3. 查看結果

分析完成後會生成：
- `spatial_map.png` - 室內空間清掃地圖
- `efficiency.png` - 清掃效率累積趨勢
- `vitals.png` - 機器人電池狀態
- `animation.gif` - 清掃路徑動畫

## ⚙️ 設定參數

在 `reconstruct_map.R` 的 `CONFIG` 區塊中可調整：

```r
CONFIG <- list(
  # 輸出尺寸 (英吋) 與 解析度
  IMG_WIDTH = 8,
  IMG_HEIGHT = 6,
  DPI = 300,

  # 字體大小設定
  BASE_FONT_SIZE = 36,
  TITLE_REL_SIZE = 2.0,

  # 顏色配置
  COLOR = list(
    FLOOR = "#F2F2F7",
    WALL = "#1C1C1E",
    PRIMARY = "#007AFF",
    ...
  ),

  # 線條粗細
  WIDTH = list(
    MAP_PATH = 1.8,
    CHART_LINE = 2.5,
    ...
  )
)
```

## 📊 分析內容

### 1. 空間地圖 (Spatial Map)
- 地板 (淺色) 和牆壁 (深色) 顯示
- 清掃路徑以漸層色彩顯示清掃進度
- 綠色圓點為起點，紅色 X 為終點

### 2. 效率分析 (Efficiency)
- X 軸：時間序列
- Y 軸：累積移動距離
- 顯示清掃覆蓋效率趨勢

### 3. 電池狀態 (Vitals)
- 清掃過程中的電量消耗預估
- Y 軸範圍 0-100%

### 4. 路徑動畫 (Animation)
- 機器人清掃路徑的動態回放
- 粉紅色點顯示機器人位置

## 📝 地圖資料格式

`map_dump.json` 包含：
- `layers[]` - 地圖圖層 (floor, wall)
- `entities[]` - 地圖實體 (path, charger_location, robot_position)
- `attributes[]` - 機器人狀態屬性
- `pixelSize` - 每像素代表的大小 (5 cm)

## 🔗 相關工具

- `map_visualizer.py` - Python 版本的地圖視覺化工具
- `mqttRover/` - MQTT 巡航控制工具

---

*最後更新: 2026-04-17*
