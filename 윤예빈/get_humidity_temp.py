import serial
import time
from datetime import datetime
from influxdb import InfluxDBClient

# InfluxDB 연결
client = InfluxDBClient(host='', username='', password='', database='')

ser = serial.Serial('/dev/ttyACM0', 9600) # 시리얼 포트 설정

def collect_data():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        
        try:
            # 데이터를 쉼표로 분리하여 습도와 온도를 각각 가져오기
            humidity, temperature = map(float, data.split(","))
            current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            
            # 습도 데이터 저장
            humidity_json = [{
                "measurement": "Humidity",
                "time": current_time,
                "fields": {
                    "humidity": humidity
                }
            }]
            client.write_points(humidity_json)
            print(f"Saved humidity: {humidity} at {current_time}")

            # 온도 데이터 저장
            temperature_json = [{
                "measurement": "Temperature",
                "time": current_time,
                "fields": {
                    "temperature": temperature
                }
            }]
            client.write_points(temperature_json)
            print(f"Saved temperature: {temperature} at {current_time}")

        except ValueError as e:
            print("Error writing Humidity, Temperature to InfluxDB:", e)

def main():
    print("Collecting humidity and temperature data...")
    try:
        while True:
            collect_data()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
