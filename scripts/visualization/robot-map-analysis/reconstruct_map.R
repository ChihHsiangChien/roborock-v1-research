# 1. 助手函數：自動載入與安裝套件 (Completed Helper)
load_packages <- function(pkgs) {
  for (pkg in pkgs) {
    if (!require(pkg, character.only = TRUE)) {
      message(paste("套件", pkg, "未找到。嘗試進行本地安裝..."))
      tryCatch(
        {
          # 取得使用者套件庫路徑
          user_lib <- Sys.getenv("R_LIBS_USER")
          if (user_lib == "") {
            user_lib <- file.path(Sys.getenv("HOME"), "R", "library")
          }
          if (!dir.exists(user_lib)) {
            dir.create(user_lib, recursive = TRUE, showWarnings = FALSE)
          }
          # 安裝並載入
          install.packages(pkg, lib = user_lib, repos = "https://cloud.r-project.org")
          library(pkg, character.only = TRUE, lib.loc = user_lib)
        },
        error = function(e) {
          stop(paste("無法安裝套件:", pkg, ". 錯誤內容:", e$message))
        }
      )
    }
  }
}

# 執行載入必要套件
required_pkgs <- c("jsonlite", "ggplot2", "dplyr", "tidyr", "gganimate", "showtext", "gifski")
load_packages(required_pkgs)

# 啟動中文字型支援 (Noto Sans TC)
font_add_google("Noto Sans TC", "noto_sans")
showtext_auto()

# 2. 載入與處理數據 (Load Data)
data <- fromJSON("map_dump.json")

# RLE 解壓縮函數
decompress_layer <- function(layer_data) {
  cp <- layer_data$compressedPixels[[1]]
  mat <- matrix(cp, ncol = 3, byrow = TRUE)
  pixels <- do.call(rbind, lapply(1:nrow(mat), function(i) {
    x_start <- mat[i, 1]
    y <- mat[i, 2]
    count <- mat[i, 3]
    data.frame(x = seq(x_start, x_start + count - 1), y = y)
  }))
  return(pixels)
}

# 處理地圖層
floor_pixels <- decompress_layer(data$map$layers[data$map$layers$type == "floor", ])
wall_pixels <- decompress_layer(data$map$layers[data$map$layers$type == "wall", ])
floor_pixels$type <- "地板 Floor"
wall_pixels$type <- "牆壁 Wall"
map_pixels <- rbind(floor_pixels, wall_pixels)

# 處理路徑
path_entity <- data$map$entities[data$map$entities$type == "path", ]
points <- path_entity$points[[1]]
path_df <- data.frame(
  x = points[seq(1, length(points), 2)] / data$map$pixelSize,
  y = points[seq(2, length(points), 2)] / data$map$pixelSize,
  t = 1:(length(points) / 2)
)

# 計算移動距離與累積距離
path_df$dist <- c(0, sqrt(diff(path_df$x)^2 + diff(path_df$y)^2))
path_df$cum_dist <- cumsum(path_df$dist)

# 3. 參數配置中心 (Configuration Center)
# 在此調整所有視覺參數，包括尺寸、顏色與字體
CONFIG <- list(
  # 輸出尺寸 (英吋) 與 解析度
  IMG_WIDTH = 8,
  IMG_HEIGHT = 6,
  DPI = 300,

  # 字體大小設定
  BASE_FONT_SIZE = 36,
  TITLE_REL_SIZE = 2.0, # 標題相對比例
  SUBTITLE_REL_SIZE = 1.5,
  LEGEND_REL_SIZE = 1.2,
  TITLE_ALIGN = 0.5, # 標題對齊方式 (0:左, 0.5:中, 1:右)

  # 顏色配置 (主要參考 Apple System Colors)
  COLOR = list(
    FLOOR = "#F2F2F7",
    WALL = "#1C1C1E",
    PATH_SCALE = "magma", # viridis 顏色系列
    PRIMARY = "#007AFF", # 藍色 (效率圖)
    WARNING = "#FF9500", # 橘色 (電池圖)
    DANGER = "#FF2D55", # 粉紅色 (動畫點)
    SUCCESS = "#34C759", # 綠色 (起點)
    STOP = "#FF3B30" # 紅色 (終點)
  ),

  # 線條與點的大小
  WIDTH = list(
    MAP_PATH = 1.8, # 地圖路徑粗細
    CHART_LINE = 2.5, # 趨勢圖線條粗細
    POINT = 6, # 標記點大小
    ANIM_POINT = 10 # 動畫中機器人的大小
  )
)

# 4. 空間地圖 (Spatial Map)
p1 <- ggplot() +
  # 底圖層
  geom_tile(data = map_pixels, aes(x, y, fill = type), alpha = 0.8) +
  # 路徑線條
  geom_path(
    data = path_df, aes(x, y, color = t, group = 1),
    linewidth = CONFIG$WIDTH$MAP_PATH, linejoin = "round", lineend = "round"
  ) +
  # 起始與結束點
  geom_point(data = path_df[1, ], aes(x, y), color = CONFIG$COLOR$SUCCESS, size = CONFIG$WIDTH$POINT) +
  geom_point(
    data = path_df[nrow(path_df), ], aes(x, y),
    color = CONFIG$COLOR$STOP, size = CONFIG$WIDTH$POINT, shape = 4, stroke = 2
  ) +
  # 顏色與填充
  scale_fill_manual(values = c("地板 Floor" = CONFIG$COLOR$FLOOR, "牆壁 Wall" = CONFIG$COLOR$WALL), name = "環境層") +
  scale_color_viridis_c(option = CONFIG$COLOR$PATH_SCALE, name = "清掃進度", direction = -1) +
  # 視覺主題
  theme_minimal(base_size = CONFIG$BASE_FONT_SIZE, base_family = "noto_sans") +
  theme(
    legend.position = "right",
    plot.title.position = "plot", # 讓標題對齊整張圖而非僅繪圖區
    plot.title = element_text(face = "bold", size = rel(CONFIG$TITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN, margin = margin(b = 15)),
    plot.subtitle = element_text(color = "gray30", size = rel(CONFIG$SUBTITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN, margin = margin(b = 20)),
    legend.text = element_text(size = rel(CONFIG$LEGEND_REL_SIZE)),
    panel.grid.major = element_line(color = "#E5E5EA"),
    panel.grid.minor = element_blank(),
    plot.background = element_rect(fill = "white", color = NA),
    plot.margin = margin(30, 30, 30, 30)
  ) +
  coord_fixed() +
  labs(
    title = "室內空間清掃地圖 Spatial Map",
    subtitle = paste("總覆蓋點數:", nrow(map_pixels), "| 路徑總長度:", round(sum(path_df$dist), 2)),
    x = "X 座標 (單位: 像素)",
    y = "Y 座標 (單位: 像素)"
  )

ggsave("spatial_map.png", p1, width = CONFIG$IMG_WIDTH, height = CONFIG$IMG_HEIGHT, dpi = CONFIG$DPI)

# 5. 效率分析 (Efficiency Analysis)
p2 <- ggplot(path_df, aes(x = t, y = cum_dist)) +
  geom_area(fill = CONFIG$COLOR$PRIMARY, alpha = 0.1) +
  geom_line(color = CONFIG$COLOR$PRIMARY, linewidth = CONFIG$WIDTH$CHART_LINE) +
  theme_minimal(base_size = CONFIG$BASE_FONT_SIZE, base_family = "noto_sans") +
  theme(
    plot.title.position = "plot",
    plot.title = element_text(face = "bold", size = rel(CONFIG$TITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN),
    plot.subtitle = element_text(size = rel(CONFIG$SUBTITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN),
    panel.grid.major = element_line(color = "#E5E5EA"),
    plot.margin = margin(30, 40, 30, 30)
  ) +
  labs(
    title = "清掃效率累積趨勢 Efficiency",
    subtitle = "時間序列與累積移動距離的關係",
    x = "時間序列 Sequence",
    y = "累積距離 Distance"
  )

ggsave("efficiency.png", p2, width = CONFIG$IMG_WIDTH, height = CONFIG$IMG_HEIGHT, dpi = CONFIG$DPI)

# 6. 電池生命體徵 (Digital Vital Signs)
battery_level <- data$attributes$level[!is.na(data$attributes$level)]
if (length(battery_level) == 0) battery_level <- 100
path_df$battery <- battery_level - (path_df$t / max(path_df$t)) * 5

p3 <- ggplot(path_df, aes(x = t, y = battery)) +
  geom_area(fill = CONFIG$COLOR$WARNING, alpha = 0.1) +
  geom_line(color = CONFIG$COLOR$WARNING, linewidth = CONFIG$WIDTH$CHART_LINE) +
  scale_y_continuous(limits = c(0, 100)) +
  theme_minimal(base_size = CONFIG$BASE_FONT_SIZE, base_family = "noto_sans") +
  theme(
    plot.title.position = "plot",
    plot.title = element_text(face = "bold", size = rel(CONFIG$TITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN),
    plot.subtitle = element_text(size = rel(CONFIG$SUBTITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN),
    panel.grid.major = element_line(color = "#E5E5EA"),
    plot.margin = margin(30, 40, 30, 30)
  ) +
  labs(
    title = "機器人電池狀態 Vital Signs",
    subtitle = "清掃過程中的電量消耗預估",
    x = "時間序列 Sequence",
    y = "電池電量 (%)"
  )

ggsave("vitals.png", p3, width = CONFIG$IMG_WIDTH, height = CONFIG$IMG_HEIGHT, dpi = CONFIG$DPI)

# 7. 路徑動畫 (Animation)
p_anim <- ggplot() +
  geom_tile(data = map_pixels, aes(x, y, fill = type), alpha = 0.3) +
  geom_path(data = path_df, aes(x, y, group = 1), color = "gray60", alpha = 0.4, linewidth = 0.8) +
  geom_point(data = path_df, aes(x, y), color = CONFIG$COLOR$DANGER, size = CONFIG$WIDTH$ANIM_POINT) +
  scale_fill_manual(values = c("地板 Floor" = CONFIG$COLOR$FLOOR, "牆壁 Wall" = CONFIG$COLOR$WALL), name = "圖層 Layer") +
  theme_minimal(base_size = CONFIG$BASE_FONT_SIZE, base_family = "noto_sans") +
  theme(
    legend.position = "none",
    plot.title.position = "plot",
    plot.title = element_text(face = "bold", size = rel(CONFIG$TITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN),
    plot.subtitle = element_text(size = rel(CONFIG$SUBTITLE_REL_SIZE), hjust = CONFIG$TITLE_ALIGN)
  ) +
  coord_fixed() +
  labs(
    title = "清掃路徑動態回放 Animation",
    subtitle = "目前步驟: {frame_time} / {nframes}",
    x = "X",
    y = "Y"
  ) +
  transition_time(t) +
  shadow_wake(wake_length = 0.1, alpha = FALSE)

anim_save("animation.gif", p_anim,
  width = CONFIG$IMG_WIDTH * 100, height = CONFIG$IMG_HEIGHT * 100,
  renderer = gifski_renderer()
)

print("已完成參數集中化版本。您可以直接調整 CONFIG 列表中的參數。")
