import time
from datetime import datetime
from influxdb import InfluxDBClient
from status_report import msg_humid_down, msg_humid_up, msg_temp_down, msg_temp_up

# 온습도 임계값
temp_threshold = 20      # 온도 임계 기본값
humidity_threshold = 50  # 습도 임계 기본값

# 온습도 임계값 설정 함수
def get_threshold():
    try:
        with open("../threshold/threshold.txt", "r") as file:
            lines = file.readlines()
            global temp_threshold, humidity_threshold
            temp_threshold = int(lines[2].strip())        # 세 번째 줄
            humidity_threshold = int(lines[3].strip())    # 네 번째 줄
    except FileNotFoundError:
        print("get_humidity_temp.py: 임계값 파일을 찾을 수 없습니다. 기본값 사용(20°C, 50%)")

def log_data_to_influxdb(measurement, value):
    """온습도 데이터를 InfluxDB에 기록"""
    data = [
        {
            "measurement": measurement,
            "fields": {
                "value": value
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

            if data_type == 'humidity_value':
                humidity_value = value
                print(f"get_humidity_temp.py: 습도 데이터 InfluxDB저장. {humidity_value}%")
                log_data_to_influxdb("Humidity", humidity_value)

            elif data_type == 'temperature_value':
                temperature_value = value
                print(f"get_humidity_temp.py: 온도 데이터 InfluxDB저장. {temperature_value}°C")
                log_data_to_influxdb("Temperature", temperature_value)
            
            # 임계값 설정
            get_threshold()

            # 온도, 습도 임계값 비교
            # 습도 임계값  +- 10% 범위
            if humidity_value < humidity_threshold - 10:
                print("get_humidity_temp.py: 습도 낮음!")
                msg_humid_down()
            elif humidity_value > humidity_threshold + 10:
                print("get_humidity_temp.py: 습도 높음!")
                msg_humid_up()

            # 온도 임계값 +- 5°C 범위
            if temperature_value < temp_threshold - 5:
                print("get_humidity_temp.py: 온도 낮음!")
                msg_temp_down()
            elif temperature_value > temp_threshold + 5:
                print("get_humidity_temp.py: 온도 높음!")
                msg_temp_up()

        time.sleep(1)  # 대기 
