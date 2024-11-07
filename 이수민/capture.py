import cv2
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("no webcam")
    exit()

try:
    while True:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            print(f"{filename} ok.")
        else:
            print("no capture")

        time.sleep(14400)

except KeyboardInterrupt:
    print("stop")

finally:
    cap.release()
    cv2.destroyAllWindows()
