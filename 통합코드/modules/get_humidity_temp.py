import time
from datetime import datetime
from influxdb import InfluxDBClient

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
        print(f"get_humidity_temp.py: Error writing {measurement} to InfluxDB:", e)
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
                print(f"습도 데이터 수신: {value}%")
                log_data_to_influxdb("Humidity", value)

            elif data_type == 'temperature_value':
                print(f"온도 데이터 수신: {value}°C")
                log_data_to_influxdb("Temperature", value)

        time.sleep(1)  # 대기 
