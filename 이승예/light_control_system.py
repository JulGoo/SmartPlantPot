from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from queue import Queue

# InfluxDB 연결 설정
client = InfluxDBClient(host='', 
                       username='', 
                       password='', 
                       database='')

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

def monitor_and_control_light(queue):
    """메인 모니터링 및 제어 함수"""
    print("Starting light sensor data collection...")
    
    last_average_check = datetime.now()  # 마지막 평균 체크 시간 초기화
    
    try:
        while True:
            if not queue.empty():
                # 큐에서 조도 데이터 받기
                data_type, value = queue.get()
                
                if data_type == 'lux_value':
                    current_time = datetime.now()
                    utc_time = datetime.utcnow()
                    time_str = utc_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # 데이터 즉시 저장
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
                    print(f"Saved lux value: {value} at {time_str}")
                    
                    # 1시간마다 평균 조도 출력
                    if current_time >= last_average_check + timedelta(hours=1):
                        avg_light = get_hourly_average()
                        if avg_light is not None:
                            print(f"\n=== 최근 1시간 평균 조도 ===")
                            print(f"시간: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                            print(f"평균 조도: {avg_light:.2f} lux\n")
                        else:
                            print("아직 데이터가 충분하지 않습니다.")
                        last_average_check = current_time
                        
    except Exception as e:
        print(f"Unexpected error in light monitoring: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_queue = Queue()
    monitor_and_control_light(test_queue)
