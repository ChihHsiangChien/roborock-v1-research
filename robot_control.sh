#!/bin/bash
#
# Roborock V1 Valetudo API 控制腳本 (修正版)
#

ROBOT="robot"
API_LOCAL="http://127.0.0.1/api/v2"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# PUT 請求函數
put_cmd() {
    local path="$1"
    local data="$2"
    ssh $ROBOT "wget -q -O - --method=PUT --body-data='$data' --header='Content-Type: application/json' '$API_LOCAL$path'" 2>/dev/null
}

cmd_status() {
    echo -e "${GREEN}取得設備狀態...${NC}"
    curl -s http://192.168.1.51/api/v2/robot/state/attributes | python3 -m json.tool 2>/dev/null || curl -s http://192.168.1.51/api/v2/robot/state/attributes
}

cmd_consumables() {
    echo -e "${GREEN}取得消耗品狀態...${NC}"
    curl -s http://192.168.1.51/api/v2/robot/capabilities/ConsumableMonitoringCapability | python3 -m json.tool 2>/dev/null || curl -s http://192.168.1.51/api/v2/robot/capabilities/ConsumableMonitoringCapability
}

cmd_statistics() {
    echo -e "${GREEN}取得統計資料...${NC}"
    local result=$(curl -s http://192.168.1.51/api/v2/robot/capabilities/TotalStatisticsCapability)
    echo "$result" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for d in data:
    if d['type'] == 'time':
        hours = d['value'] // 3600
        print(f'總清掃時間: {hours} 小時 ({d[\"value\"]} 秒)')
    elif d['type'] == 'area':
        sqm = d['value'] / 1000000
        print(f'總清掃面積: {sqm:.2f} 平方公尺')
    elif d['type'] == 'count':
        print(f'總清掃次數: {d[\"value\"]} 次')
"
}

cmd_locate() {
    echo -e "${GREEN}定位機器人...${NC}"
    put_cmd "/robot/capabilities/LocateCapability" '{"action":"locate"}'
    echo -e "${GREEN}完成!${NC}"
}

cmd_start() {
    echo -e "${GREEN}開始清掃...${NC}"
    put_cmd "/robot/capabilities/BasicControlCapability" '{"action":"start"}'
    echo -e "${GREEN}清掃已開始!${NC}"
}

cmd_pause() {
    echo -e "${GREEN}暫停清掃...${NC}"
    put_cmd "/robot/capabilities/BasicControlCapability" '{"action":"pause"}'
    echo -e "${GREEN}已暫停!${NC}"
}

cmd_stop() {
    echo -e "${GREEN}停止清掃...${NC}"
    put_cmd "/robot/capabilities/BasicControlCapability" '{"action":"stop"}'
    echo -e "${GREEN}已停止!${NC}"
}

cmd_home() {
    echo -e "${GREEN}返回充電座...${NC}"
    put_cmd "/robot/capabilities/BasicControlCapability" '{"action":"home"}'
    echo -e "${GREEN}正在返回...${NC}"
}

cmd_fan() {
    local level=${1:-medium}
    echo -e "${GREEN}設定風扇為 $level...${NC}"
    put_cmd "/robot/capabilities/FanSpeedControlCapability/preset" "{\"name\":\"$level\"}"
    echo -e "${GREEN}風扇已設定為 $level!${NC}"
}

cmd_fan_presets() {
    echo -e "${GREEN}可用風扇預設值:${NC}"
    curl -s http://192.168.1.51/api/v2/robot/capabilities/FanSpeedControlCapability/presets
    echo ""
}

cmd_reset_consumable() {
    local type=$1
    local subtype=$2
    if [ -z "$type" ] || [ -z "$subtype" ]; then
        echo -e "${RED}用法: $0 reset <brush|filter|cleaning> <main|side_right|sensor>${NC}"
        return 1
    fi
    echo -e "${GREEN}重置消耗品: $type/$subtype${NC}"
    put_cmd "/robot/capabilities/ConsumableMonitoringCapability" "{\"consumable\":{\"type\":\"$type\",\"subType\":\"$subtype\"},\"action\":\"reset\"}"
    echo -e "${GREEN}已重置!${NC}"
}

case "${1:-}" in
    status)      cmd_status ;;
    consumables) cmd_consumables ;;
    stats)       cmd_statistics ;;
    locate)      cmd_locate ;;
    start)       cmd_start ;;
    pause)       cmd_pause ;;
    stop)        cmd_stop ;;
    home|charge) cmd_home ;;
    fan)         cmd_fan "$2" ;;
    fan-presets) cmd_fan_presets ;;
    reset)        cmd_reset_consumable "$2" "$3" ;;
    *)
        echo "用法: $0 {status|consumables|stats|locate|start|pause|stop|home|fan [level]|fan-presets|reset <type> <subtype>}"
        echo ""
        echo "範例:"
        echo "  $0 status          # 取得狀態"
        echo "  $0 consumables     # 取得消耗品"
        echo "  $0 stats           # 取得統計"
        echo "  $0 start           # 開始清掃"
        echo "  $0 home            # 返回充電座"
        echo "  $0 fan max         # 設定風扇為 max"
        echo "  $0 fan-presets     # 顯示可用預設值"
        echo "  $0 reset brush main # 重置主刷"
        exit 1
        ;;
esac
