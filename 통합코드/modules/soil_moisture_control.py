import time
from datetime import datetime
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from modules.water_tank_monitor import log_water_tank_level, get_tank_level_percent
from modules.status_report import msg_water
import asyncio

# GPIO 설정
MOTER_PIN = 14  # 수중 모터 핀(우측위에서 3번째)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTER_PIN, GPIO.OUT)

# InfluxDB 연결 설정
client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='spp')

# 토양 습도 퍼센트 임계값 설정 함수
def get_moisture_threshold():
    moisture_threshold = 30  # 기본값
    try:
        with open("/home/pi/SmartPlantPot/threshold/threshold.txt", "r") as file:
            lines = file.readlines()
            threshold = lines[0].strip()    # 첫번째 줄만 읽기
            moisture_threshold = int(threshold)
    except FileNotFoundError:
        print("soil_moisture_control.py: 토양습도 임계값 파일을 찾을 수 없습니다. 기본 임계값을 사용합니다.")
    return moisture_threshold

# 토양 습도 퍼센트 변환 함수
def get_soil_moisture_percent(soil_moisture):
    return int((soil_moisture / 700) * 100)  # 최대 값 1023/실제 최대 값과 비교 필요

# 토양 습도 값 기록 함수
def log_soil_moisture(soil_moisture):
    data = [
        {
            "measurement": "Soil_moisture",
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "soil_moisture": soil_moisture
            }
        }
    ]
    try:
        client.write_points(data)
        print(f"soil_moisture_control.py: 토양습도 데이터 InfluxDB저장. {soil_moisture}%")

    except Exception as e:
        print("soil_moisture_control.py: InfluxDB 에러", e)
    finally:
        if client is not None:
            client.close()

# 물 공급 함수
def activate_water_pump():
    GPIO.output(MOTER_PIN, GPIO.LOW)  # 모터 ON
    time.sleep(2)  # 물 공급 시간
    GPIO.output(MOTER_PIN, GPIO.HIGH)  # 모터 OFF

    log_water_tank_level(get_tank_level_percent())    # 물탱크 수위 최신화

# 토양 습도 제어
def monitor_and_control_soil_moisture(queue):
    while True:
        if not queue.empty():        
            # 큐에서 토양 습도 데이터 받기
            data_type, value = queue.get()
            queue.queue.clear()  # 큐 비우기
            print(f"soil_moisture_control.py: Get Queue Value: data_type={data_type}, value={value}")  # 디버깅용 출력

            if data_type == 'soil_moisture_value':
                soil_moisture = value

                # 토양 습도 계산
                soil_moisture_percent = get_soil_moisture_percent(soil_moisture)

                print('soil_moisture_control.py: 토양습도 퍼센트(', soil_moisture_percent, "%)")

                # 토양 습도 기록
                log_soil_moisture(soil_moisture_percent)
                #asyncio.run(msg_water())

                # 임계값 비교 후 물 공급
                if soil_moisture_percent < get_moisture_threshold():
                    activate_water_pump()
                    print("soil_moisture_control.py: 토양 습도 임계값보다 낮음, 모터 작동")
                    
        #time.sleep(5)  # 대기(테스트)
        time.sleep(600)  # 대기(10분)
