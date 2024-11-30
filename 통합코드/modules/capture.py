import threading
import cv2
import time
import os
from influxdb import InfluxDBClient
from datetime import datetime

# 이미지 저장 경로
save_directory = "/home/pi/SmartPlantPot/plant_images"

# 이미지 저장 주기
capture_interval = 3 * 60 * 60  # (3시간)

# 주간, 야간
DAYTIME_START = 6   # 오전 6시
DAYTIME_END = 18    # 오후 6시

# 주간인지 확인
def is_daytime():
    """현재 시간이 주간인지 확인"""
    current_hour = datetime.now().hour
    return DAYTIME_START <= current_hour < DAYTIME_END

def capture_photos_from_webcam():
    client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='spp')

    cap = cv2.VideoCapture(0)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    if not cap.isOpened():
        print("capture.py: 웹캠 연결 실패")
        return

    try:
        while True:
            # 주간 시간대인지 확인
            if is_daytime():
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}.jpg"

                ret, frame = cap.read()
                if ret:
                    # 이미지를 지정된 경로에 저장
                    cv2.imwrite(os.path.join(save_directory, filename), frame)
                    print(f"capture.py: 이미지 저장 완료 '/plant_images/{filename}' ")

                    # InfluxDB에 데이터 저장
                    json_body = [
                        {
                            "measurement": "photos",
                            "tags": {
                                "source": "webcam"
                            },
                            "fields": {
                                "filename": filename,
                                "timestamp": timestamp
                            }
                        }
                    ]
                    client.write_points(json_body)
                else:
                    print("capture.py: 이미지 저장 실패")
            else:
                # 야간 시간대에서 주기적으로 메시지 출력
                print("capture.py: 야간 시간대 - 웹캠 작동 제한")

            # 주기적으로 이미지 캡처를 시도
            time.sleep(capture_interval)

    except KeyboardInterrupt:
        print("capture.py: KeyboardInterrupt")

    finally:
        cap.release()
        cv2.destroyAllWindows()