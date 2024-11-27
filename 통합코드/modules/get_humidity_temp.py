import time
from datetime import datetime
from influxdb import InfluxDBClient
from modules.status_report import msg_humid_down, msg_humid_up, msg_temp_down, msg_temp_up
import asyncio

# 온습도 임계값
temp_threshold = 20      # 온도 임계 기본값
humidity_threshold = 50  # 습도 임계 기본값

# 온습도 임계값 설정 함수
def get_threshold():
    try:
        with open("/home/pi/SmartPlantPot/threshold/threshold.txt", "r") as file:
            lines = file.readlines()
            global temp_threshold, humidity_threshold
            temp_threshold = int(lines[2].strip())        # 세 번째 줄
            humidity_threshold = int(lines[3].strip())    # 네 번째 줄
    except FileNotFoundError:
        print("get_humidity_temp.py: 임계값 파일을 찾을 수 없습니다. 기본값 사용(20°C, 50%)")

def log_data_to_influxdb(measurement, field_name, value):
    """온습도 데이터를 InfluxDB에 기록"""
    data = [
        {
            "measurement": measurement,
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                field_name: value
            }
        }
    ]
    client = None
    try:
        client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='spp')
        client.write_points(data)
    except Exception as e:
        print(f"get_humidity_temp.py: InfluxDB 에러", e)
    finally:
        if client:
            client.close()

def monitor_and_log_temperature_humidity(queue):
    """큐에서 온도 및 습도 데이터를 읽고 InfluxDB에 기록"""
    while True:
        if not queue.empty():
            # 큐에서 데이터 읽기
            data_type, value = queue.get()
            queue.queue.clear()  # 큐 비우기
            print(f"get_humidity_temp.py: Get Queue Value: data_type={data_type}, value={value}")  # 디버깅용 출력

            if data_type == 'temp_humidity_value':
                temperature_value, humidity_value = value  # 튜플 언패킹

                # 온도 처리
                print(f"get_humidity_temp.py: 온도 데이터 InfluxDB저장. {temperature_value}°C")
                log_data_to_influxdb("Temperature", "temperature", temperature_value)

                if temperature_value < temp_threshold - 5:
                    print("get_humidity_temp.py: 습도 낮음")
                    # asyncio.run(msg_temp_down())
                elif temperature_value > temp_threshold + 5:
                    print("get_humidity_temp.py: 습도 높음")
                    # asyncio.run(msg_temp_up())

                # 습도 처리
                print(f"get_humidity_temp.py: 습도 데이터 InfluxDB저장.  {humidity_value}%")
                log_data_to_influxdb("Humidity", "humidity", humidity_value)

                if humidity_value < humidity_threshold - 10:
                    print("get_humidity_temp.py: 온도 낮음")
                    #asyncio.run(msg_humid_down())
                elif humidity_value > humidity_threshold + 10:
                    print("get_humidity_temp.py: 온도 높음")
                    #asyncio.run(msg_humid_up())

            # 임계값 설정
            get_threshold()

            # 온도, 습도 임계값 비교
            # 습도 임계값  +- 10% 범위

            # 온도 임계값 +- 5°C 범위

        #time.sleep(5)  # 대기(테스트)
        time.sleep(600)  # 대기(10분)
