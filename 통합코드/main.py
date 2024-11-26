import threading
import time
import serial
from queue import LifoQueue
import modules
import asyncio

# 시리얼 포트 설정
serial_port = '/dev/ttyACM0'  # 아두이노 시리얼 포트
baud_rate = 9600  # 보드레이트

# 센서 값을 전달하기 위한 스레드 각각의 큐
queue_1 = LifoQueue()
queue_2 = LifoQueue()
queue_3 = LifoQueue()
queue_4 = LifoQueue()

def serial_reader():
    """시리얼 데이터를 읽어서 큐에 전달하는 스레드"""
    ser = serial.Serial(serial_port, baud_rate)
    while True:
        if ser.in_waiting > 0:
            
            line = ser.readline().decode('utf-8').rstrip()
            parts = line.split(',')

            print(line)
            # 큐에 데이터 넣기
            queue_1.put(('soil_moisture_value', int(parts[0])))	# 첫 번째 값: 토양 습도
            queue_2.put(('water_tank_value', int(parts[1])))	# 두 번째 값: 물탱크 거
            queue_3.put(('lux_value', int(parts[2])))	# 세 번째 값: 조도
            queue_4.put(('temp_humidity_value', (int(parts[3]), int(parts[4]))))  # 네 번째 값: 온도, 다섯 번째 값: 습도

        time.sleep(1)  # 시리얼 데이터를 읽는 주기 (1초)

def start_threads():
    """멀티스레드 실행"""
    # 시리얼 읽기 스레드
    serial_thread = threading.Thread(target=serial_reader, daemon=True)

    # 토양 습도 제어 스레드
    soil_moisture_thread = threading.Thread(target=modules.monitor_and_control_soil_moisture, args=(queue_1,), daemon=True)

    # 물탱크 수위 기록 스레드
    water_tank_thread = threading.Thread(target=modules.monitor_and_log_water_tank_level, args=(queue_2,), daemon=True)

	# 일조량 제어 스레드
    light_thread = threading.Thread(target=modules.monitor_and_control_light, args=(queue_3,), daemon=True)
	
	# 온습도 기록 스레드
    temperature_humidity_thread = threading.Thread(target=modules.monitor_and_log_temperature_humidity, args=(queue_4,), daemon=True)
	
	# 카메라 촬영 스레드
    capture_photos_thred = threading.Thread(target=modules.capture_photos_from_webcam, daemon=True)

	# 사용자 인터페이스 스레드(비동기 실행)
    telegram_userinterface_thread = threading.Thread(target=run_asyncio_in_thread, daemon=True)

    # 스레드 시작
    serial_thread.start()
    soil_moisture_thread.start()
    water_tank_thread.start()
    light_thread.start()
    temperature_humidity_thread.start()
    capture_photos_thred.start()
    telegram_userinterface_thread.start()

    # 메인 스레드는 계속 실행되어야 함
    serial_thread.join()
    soil_moisture_thread.join()
    water_tank_thread.join()
    light_thread.join()
    temperature_humidity_thread.join()
    capture_photos_thred.join()
    telegram_userinterface_thread.start()

# 텔레그램 사용자 인터페이스 비동기 실행 함수
def run_asyncio_in_thread():
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(modules.main())

if __name__ == "__main__":
    try:
        print("**Smart Plant Pot Program Start**")
        start_threads()
    except KeyboardInterrupt:
        print("main.py: Program interrupted.")
