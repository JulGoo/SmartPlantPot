import serial
import time
from datetime import datetime
from influxdb import InfluxDBClient
# InfluxDB 연결 설정
client = InfluxDBClient(host='', username='', password='', database='')
# 시리얼 포트 연결
ser = serial.Serial('/dev/ttyACM0', 9600)
def collect_data():
    """조도 센서 데이터 수집 및 DB 저장"""
    if ser.in_waiting > 0:
        try:
            # 시리얼 데이터 읽기 및 정수로 변환
            lux_value = int(float(ser.readline().decode('utf-8').strip()))
            current_time = datetime.utcnow()
            time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            # InfluxDB에 데이터 저장
            json_body = [
                {
                    "measurement": "Light_Exposure",
                    "time": current_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "fields": {
                        "lux": lux_value
                    }
                }
            ]
            client.write_points(json_body)
            print(f"Saved lux value: {lux_value} at {time_str}")
            return lux_value
        except ValueError as e:
            print(e)
            print("Invalid sensor reading")
            return None
def main():
    print("Starting light sensor data collection...")

    try:
        while True:
            collect_data()
            time.sleep(20)  # 20초 간격으로 데이터 수집

    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        ser.close()
if name == "main":
    main()
