import serial
import time
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient as influxdb

# 수중 모터 핀 설정
motor_pin = 14  # GPIO 핀 번호

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)

# 시리얼 포트 설정
serial_port = '/dev/ttyACM0' 	# 포트
baud_rate = 9600  		# 보드레이트
ser = serial.Serial(serial_port, baud_rate)

# 토양 습도 임계값 설정
moisture_threshold = 200 

# InfluxDB 설정
def influxDB_insert(soil_moisture, distance):
    data = [
        {
            "measurement": "soil_moisture",
            "tags": {
                "location": "soil_moisture_water_tank_moniter",
                "input": "soil_moisture_sensor",
                "output": "water_moter"
            },
            "fields": {
                "soil_moisture": soil_moisture,
            }
        },
        {
            "measurement": "water_tank_distance",
            "tags": {
                "location": "soil_moisture_water_tank_moniter",
                "input": "ultrasonic_sensor"
            },
            "fields": {
                "water_tank_distance": distance
            }
        }
    ]
    
    # InfluxDB 연결 및 데이터 전송
    client = None
    try:
        client = influxdb('localhost', 8086, 'root', 'root', 'SmartPlantPot')
    except Exception as e:
        print("InfluxDB Exception: " + str(e))
    
    if client is not None:
        try:
            client.write_points(data)
        except Exception as e:
            print("InfluxDB Exception write: " + str(e))
        finally:
            client.close()

try:
    while True:
        # 시리얼 데이터 읽기
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip() 
            print(line)  # 수신된 데이터 출력

            # 데이터 파싱
            parts = line.split(' ')
            soil_moisture = int(parts[1])  # 토양 습도 값
            distance = float(parts[3])  	# 거리 값

            # InfluxDB에 데이터 저장
            influxDB_insert(soil_moisture, distance)    

            # 토양 습도 값에 따라 모터 작동
            if soil_moisture < moisture_threshold:
                print("모터 작동")
                GPIO.output(motor_pin, GPIO.LOW)  # 모터 ON
            else:
                print("모터 정지")
                GPIO.output(motor_pin, GPIO.HIGH)  # 모터 OFF

        time.sleep(3)  # 3초 대기

except KeyboardInterrupt:
    print("종료")
finally:
    GPIO.cleanup()
    ser.close()
