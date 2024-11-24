from datetime import datetime, timedelta
from influxdb import InfluxDBClient
import time
from queue import Queue
from pi5neo import Pi5Neo

# LED 설정
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# 수동 제어 변수
manual_control = False

# 조도 설정
DAYTIME_START = 6   # 오전 6시
DAYTIME_END = 18    # 오후 6시

# 밝기 프리셋 정의 (0-255 범위로 변환)
BRIGHTNESS_PRESETS = {
    25: 64,    # 25% = 64 (255 * 0.25)
    50: 128,   # 50% = 128 (255 * 0.50)
    75: 191,   # 75% = 191 (255 * 0.75)
    100: 255   # 100% = 255 (255 * 1.00)
}

# 수동 조명 제어 (LED를 지정된 밝기 퍼센트로 켜기)
def turn_on_led_with_brightness(brightness_percent):  
    global manual_control
    try:
        if brightness_percent not in BRIGHTNESS_PRESETS:
            print(f"잘못된 밝기 값입니다. 25, 50, 75, 100 중 선택하세요.")
            return False
            
        manual_control = True
        brightness = BRIGHTNESS_PRESETS[brightness_percent]
        neo.clear_strip()
        neo.fill_strip(brightness, brightness, brightness)
        neo.update_strip()
        print(f"LED 밝기가 {brightness_percent}%로 설정되었습니다.")
        return True
    except Exception as e:
        print(f"LED 켜기 실패")
        return False

# 수동 조명 제어(LED OFF)
def turn_off_led():
    try:
        neo.clear_strip()
        neo.fill_strip(0, 0, 0)  # LED 끄기
        neo.update_strip()
        return True
    except Exception as e:
        print(f"LED 끄기 실패")
        return False

# 자동 모드 전환 함수
def switch_to_auto_mode():
    global manual_control
    try:
        manual_control = False
        print("자동 모드로 전환되었습니다.")
        return True
    except Exception as e:
        print(f"모드 전환 실패")
        return False

# 조도 임계값 설정 함수
def get_light_threshold():
    light_threshold = 20000    # 기본값
    try:
        with open("threshold.txt", "r") as file:
            lines = file.readlines()
            threshold = lines[1].strip()    # 두번째 줄만 읽기
            light_threshold = int(threshold)
    except FileNotFoundError:
        print("조도 임계값 파일을 찾을 수 없습니다. 기본 임계값을 사용합니다.")
    return light_threshold

# InfluxDB 연결 설정
client = InfluxDBClient(host='', 
                       username='', 
                       password='', 
                       database='')

def is_daytime():
    """현재 시간이 주간인지 확인"""
    current_hour = datetime.now().hour
    return DAYTIME_START <= current_hour < DAYTIME_END

def get_hourly_average():
    """최근 1시간 조도 데이터의 평균 계산"""
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    
    query = f'''
    SELECT mean("lux") 
    FROM "Light_Exposure" 
    WHERE time >= '{one_hour_ago.strftime('%Y-%m-%dT%H:%M:%SZ')}'
    '''
    
    result = client.query(query)
    points = list(result.get_points())
    return points[0]['mean'] if points and points[0]['mean'] is not None else None

def calculate_led_brightness(current_lux):
    """부족한 조도에 따른 LED 밝기 계산"""
    light_threshold = get_light_threshold()  # 임계값 읽기
   
    if current_lux >= light_threshold:
        return 0

    # 부족한 조도량에 비례하여 LED 밝기 설정
    lux_deficit = light_threshold - current_lux
    # LED 밝기를 0-255 범위로 매핑
    brightness = int((lux_deficit / light_threshold) * 255)
    return min(brightness, 255) # 최대 255로 제한

def control_leds(brightness):
    """LED 밝기 제어"""
    neo.clear_strip()
    neo.fill_strip(brightness, brightness, brightness)
    neo.update_strip()



def monitor_and_control_light(queue):
    """메인 모니터링 및 제어 함수"""
    # print("Starting light sensor data collection...")
    
    last_average_check = datetime.now()  # 마지막 평균 체크 시간 초기화
    led_control_end_time = None # LED 제어 종료 시간
    
    try:
        while True:
            if not queue.empty(): 
                # 큐에서 조도 데이터 받기
                data_type, value = queue.get()
                
                if data_type == 'lux_value':
                    current_time = datetime.now()
                    utc_time = datetime.utcnow()
                    
                    # 데이터 저장
                    json_body = [
                        {
                            "measurement": "Light_Exposure",
                            "time": utc_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                            "fields": {
                                "lux": value
                            }
                        }
                    ]
                    client.write_points(json_body)
                    print(f"Saved lux value: {value}")
                    
		    
                    # 수동 모드가 아닐 때만 자동 제어 실행
                    if not manual_control:
                        # 1시간마다 평균 조도 확인 및 LED 제어
                        if current_time >= last_average_check + timedelta(hours=1):
                            avg_light = get_hourly_average()
                            if avg_light is not None:
                                print(f"\n=== 최근 1시간 평균 조도 ===")
                                print(f"시간: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                                print(f"평균 조도: {avg_light:.2f} lux")

                                # 주간 시간대이고 조도가 부족한 경우에만 LED 작동
                                if is_daytime():
                                    brightness = calculate_led_brightness(avg_light)
                                    if brightness > 0:
                                        print(f"조도 부족 감지 - LED 밝기 설정: {brightness}")
                                        control_leds(brightness)
                                        led_control_end_time = current_time + timedelta(hours=1)
                                    else:
                                        print("충분한 조도 - LED 꺼짐")
                                        control_leds(0)
                                else:
                                    print("야간 시간대 - LED 작동 제한")
                                    control_leds(0)

                            last_average_check = current_time

                        # LED 작동 시간 체크 (자동 모드일 때만)
                        if led_control_end_time and current_time >= led_control_end_time:
                            print("LED 작동 시간 종료")
                            control_leds(0)
                            led_control_end_time = None

            time.sleep(0.1)
                        
    except Exception as e:
        print(f"Unexpected error in light monitoring: {e}")
    finally:
        if not manual_control:
            control_leds(0)
        client.close()

if __name__ == "__main__":
    test_queue = Queue()
    monitor_and_control_light(test_queue)
