import cv2
import time
import os
from influxdb import InfluxDBClient

# 이미지 저장 경로
save_directory ="/home/pi/SmartPlantPot/plant_images"

# 이미지 저장 주기
capture_interval = 14400    # (4시간)

def capture_photos_from_webcam():

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
