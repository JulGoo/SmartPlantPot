import cv2
import time
import os
from influxdb import InfluxDBClient
from datetime import datetime

# 이미지 저장 경로
save_directory ="/home/pi/SmartPlantPot/plant_images"

# 이미지 저장 주기
capture_interval = 3 * 60 * 60    # (3시간)

# 주간, 야간
DAYTIME_START = 6   # 오전 6시
DAYTIME_END = 18    # 오후 6시

# 주간인지 확인
def is_daytime():
    """현재 시간이 주간인지 확인"""
    current_hour = datetime.now().hour
    return DAYTIME_START <= current_hour < DAYTIME_END

def capture_photos_from_webcam():

    if is_daytime():
        client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='spp')

        cap = cv2.VideoCapture(0)

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)


        if not cap.isOpened():
            print("captuer.py: 웹캠 연결 실패")
            exit()

        try:
            while True:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}.jpg"

                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(os.path.join(save_directory, filename), frame)
                    print(f"captuer.py: 이미지 저장 완료 '/plant_images/{filename}' ")

                    json_body = [
                            {
                                "measurement":"photos",
                                "tags":{
                                    "source":"webcam"
                                    },
                                "fields":{
                                    "filename":filename,
                                    "timestamp":timestamp
                                    }
                                }
                            ]
                    client.write_points(json_body)
                else:
                    print("captuer.py: 이미지 저장 실패")

                time.sleep(capture_interval)

        except KeyboardInterrupt:
            print("captuer.py: KeyboardInterrupt")

        finally:
            cap.release()
            cv2.destroyAllWindows()

    else:
        print("captuer.py: 야간 시간대 - 웹캠 작동 제한")
