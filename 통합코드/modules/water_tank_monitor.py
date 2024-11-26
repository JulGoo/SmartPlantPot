import time
from influxdb import InfluxDBClient
from modules.status_report import msg_water_tank
import asyncio

# 물탱크 높이 설정
TANK_HEIGHT_CM = 22  # 물탱크 높이 (cm)

# 물탱크 퍼센트
tank_leverl_percent = 0  # 물탱크 수위 퍼센트

# 물탱크 센서 값
water_tank_value = 0

# InfluxDB 연결 설정
client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='spp')

# 물탱크 수위 퍼센트 변환 함수
def get_tank_level_percent():
    water_height = TANK_HEIGHT_CM - water_tank_value
    level_percent = max(0, min(100, (water_height / TANK_HEIGHT_CM) * 100))
    return int(level_percent)

# 물탱크 수위 퍼센트 반환 함수
def get_current_tank_level_percent():
    return tank_leverl_percent

# 물탱크 수위 기록 함수
def log_water_tank_level(level_percent):
    data = [
        {
            "measurement": "water_tank_level",
            "fields": {
                "level_percent": level_percent
            }
        }
    ]
    try:
        client.write_points(data)
        print(f"water_tank_monitor.py: 물탱크 수위 데이터 InfluxDB저장. {level_percent}%")

    except Exception as e:
        print("water_tank_monitor.py: InfluxDB 에러", e)
    finally:
        if client is not None:
            client.close()

# 물탱크 수위 확인 및 기록
def monitor_and_log_water_tank_level(queue):
    while True:
        if not queue.empty():
            data_type, value = queue.get()
            queue.clear()  # 큐 비우기
            print(f"water_tank_monitorl.py: Get Queue Value: data_type={data_type}, value={value}")  # 디버깅용 출력

            if data_type == 'water_tank_value':
                global water_tank_value 
                water_tank_value = value

                # 물탱크 수위 계산
                level_percent = get_tank_level_percent()

                if(level_percent <= 10):
                    print('water_tank_monitor.py: 물탱크 수위가 10% 이하')
                    #asyncio.run(msg_water_tank())    # 텔레그램 물탱크 물 부족 알람

                # 물탱크 수위 기록
                log_water_tank_level(level_percent)

        time.sleep(1)  # 대기(테스트)
        #time.sleep(3600)  # 대기(1시간)
