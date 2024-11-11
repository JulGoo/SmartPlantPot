import cv2
import time
import os
from influxdb import InfluxDBClient

client = InfluxDBClient(host='mojuk.kr', port=8086, username='admin', password='pw.1234', database='spp')

cap = cv2.VideoCapture(0)

save_directory ="/home/pi/timelapse"

if not os.path.exists(save_directory):
    os.makedirs(save_directory)


if not cap.isOpened():
    print("no webcam")
    exit()

try:
    while True:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(os.path.join(save_directory, filename), frame)
            print(f"{filename} ok.")

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
            print(f"{filename} store ok")
        else:
            print("no capture")

        time.sleep(10)

except KeyboardInterrupt:
    print("stop")

finally:
    cap.release()
    cv2.destroyAllWindows()
