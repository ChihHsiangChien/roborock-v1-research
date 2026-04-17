#!/usr/bin/env python3
"""
Roborock V1 Valetudo API 客戶端
已驗證可用
"""

import urllib.request
import urllib.error
import json
import subprocess
from typing import Dict, List, Any, Optional

class ValetudoClient:
    """Valetudo REST API 客戶端"""
    
    def __init__(self, host: str = "192.168.1.51", ssh_host: str = "robot"):
        self.host = host
        self.ssh_host = ssh_host
        self.base_url = f"http://{host}"
        
    def _get(self, path: str) -> Optional[Any]:
        """執行 GET 請求"""
        url = f"{self.base_url}{path}"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f"GET {path} failed: {e}")
            return None
    
    def _put(self, path: str, data: Dict) -> bool:
        """執行 PUT 請求 (透過 SSH)"""
        # 直接呼叫 bash 腳本
        try:
            result = subprocess.run(
                ['/home/student/robot/robot_control.sh', 'api', path, json.dumps(data)],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            print(f"PUT {path} failed: {e}")
            return False
    
    def _put_simple(self, cmd: str) -> bool:
        """直接執行控制命令"""
        try:
            result = subprocess.run(
                ['/home/student/robot/robot_control.sh'] + cmd.split(),
                capture_output=True, text=True, timeout=15
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Command failed: {e}")
            return False
    
    def get_capabilities(self) -> List[str]:
        """取得設備能力列表"""
        return self._get("/api/v2/robot/capabilities") or []
    
    def get_state(self) -> List[Dict]:
        """取得設備狀態"""
        return self._get("/api/v2/robot/state/attributes") or []
    
    def get_status_text(self) -> str:
        """取得人類可讀的狀態"""
        state = self.get_state()
        for attr in state:
            if attr.get('__class') == 'StatusStateAttribute':
                return attr.get('value', 'unknown')
        return 'unknown'
    
    def get_battery_level(self) -> int:
        """取得電量百分比"""
        state = self.get_state()
        for attr in state:
            if attr.get('__class') == 'BatteryStateAttribute':
                return attr.get('level', 0)
        return 0
    
    def get_fan_speed(self) -> str:
        """取得當前風扇速度"""
        state = self.get_state()
        for attr in state:
            if attr.get('__class') == 'PresetSelectionStateAttribute':
                if attr.get('type') == 'fan_speed':
                    return attr.get('value', 'unknown')
        return 'unknown'
    
    def get_consumables(self) -> List[Dict]:
        """取得消耗品狀態"""
        return self._get("/api/v2/robot/capabilities/ConsumableMonitoringCapability") or []
    
    def get_statistics(self) -> Dict:
        """取得統計資料"""
        data = self._get("/api/v2/robot/capabilities/TotalStatisticsCapability") or []
        result = {}
        for item in data:
            t = item.get('type')
            v = item.get('value', 0)
            if t == 'time':
                result['time_hours'] = round(v / 3600, 1)
                result['time_seconds'] = v
            elif t == 'area':
                result['area_sqm'] = round(v / 1000000, 2)
            elif t == 'count':
                result['count'] = v
        return result
    
    def get_wifi_status(self) -> Dict:
        """取得 WiFi 狀態"""
        return self._get("/api/v2/robot/capabilities/WifiConfigurationCapability") or {}
    
    def get_fan_presets(self) -> List[str]:
        """取得風扇預設值"""
        return self._get("/api/v2/robot/capabilities/FanSpeedControlCapability/presets") or []
    
    def start(self) -> bool:
        """開始清掃"""
        return self._put_simple("start")
    
    def pause(self) -> bool:
        """暫停清掃"""
        return self._put_simple("pause")
    
    def stop(self) -> bool:
        """停止清掃"""
        return self._put_simple("stop")
    
    def home(self) -> bool:
        """返回充電座"""
        return self._put_simple("home")
    
    def locate(self) -> bool:
        """定位機器人 (發出聲音)"""
        return self._put_simple("locate")
    
    def set_fan_speed(self, preset: str) -> bool:
        """設定風扇速度 (min/low/medium/high/max)"""
        return self._put_simple(f"fan {preset}")
    
    def reset_consumable(self, type_: str, sub_type: str) -> bool:
        """重置消耗品計時器
        
        Args:
            type_: brush, filter, cleaning
            sub_type: main, side_right, sensor
        """
        return self._put_simple(f"reset {type_} {sub_type}")
    
    def print_info(self):
        """列印設備資訊"""
        print("=" * 50)
        print("Roborock V1 設備資訊")
        print("=" * 50)
        
        print(f"\n狀態: {self.get_status_text()}")
        print(f"電量: {self.get_battery_level()}%")
        print(f"風扇: {self.get_fan_speed()}")
        
        print("\n消耗品:")
        for c in self.get_consumables():
            remaining = c.get('remaining', {})
            type_ = c.get('type', '')
            subtype = c.get('subType', '')
            value = remaining.get('value', 0)
            unit = remaining.get('unit', '')
            if unit == 'minutes':
                hours = value // 60
                print(f"  {type_}/{subtype}: {hours} 小時")
            else:
                print(f"  {type_}/{subtype}: {value} {unit}")
        
        print("\n統計:")
        stats = self.get_statistics()
        print(f"  總清掃時間: {stats.get('time_hours', 0)} 小時")
        print(f"  總清掃面積: {stats.get('area_sqm', 0)} 平方公尺")
        print(f"  總清掃次數: {stats.get('count', 0)} 次")
        
        print("\n風扇預設值:", self.get_fan_presets())
        print("=" * 50)


# 使用範例
if __name__ == "__main__":
    client = ValetudoClient()
    
    # 印出裝置資訊
    client.print_info()
    
    # 示範控制命令 (取消註釋以執行)
    print("\n控制命令示範:")
    print("-" * 30)
    
    # 定位機器人
    print("定位機器人...")
    if client.locate():
        print("  ✓ 成功")
    else:
        print("  ✗ 失敗")
    
    # 設定風扇
    print("設定風扇為 medium...")
    if client.set_fan_speed("medium"):
        print("  ✓ 成功")
    else:
        print("  ✗ 失敗")
    
    # 返回充電座
    print("返回充電座...")
    if client.home():
        print("  ✓ 成功")
    else:
        print("  ✗ 失敗")
