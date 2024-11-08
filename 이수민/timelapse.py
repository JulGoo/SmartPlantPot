import cv2
import os
import glob
from datetime import datetime, timedelta

def create_video_from_photos(start_date, end_date, output_filename):
    print("make...")

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    photo_directory = '/home/pi/timelapse'
    photos = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        filename_pattern = f"photo_{date_str}_*.jpg"
        matching_files = glob.glob(os.path.join(photo_directory, filename_pattern))
        photos.extend(matching_files)
        print(f"{current_date.strftime('&Y-%m-%d')} search : {matching_files}")
        current_date += timedelta(days=1)

    if not photos:
        print("no photo")
        return

    print(f"fine photo : {photos}")
    
    if not photos:
        print("use photo no")
        return

    first_frame = cv2.imread(photos[0])
    if first_frame is None:
        print("first photo read no")
        return

    height, width, layers = first_frame.shape
    video = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'XVID'), 5, (width, height))

    for photo in sorted(photos):
        print(f"read photo:{photo}")
        frame = cv2.imread(photo)
        if frame is None:
            print(f"no frame : {photo}")
            continue
 
        frame_resized = cv2.resize(frame, (width, height))
        print(f"{photo} size : {frame.shape} -> resize : {frame_resized.shape}")

        video.write(frame)
        print(f"{photo} add.")

    video.release()
    print(f"{output_filename} make ok. file size : {os.path.getsize(output_filename)} bytes")

start_date = "2024-11-07"
end_date = "2024-11-08"
output_filename = "/home/pi/timelapse/output_video.mp4"

try:
    create_video_from_photos(start_date, end_date, output_filename)
except Exception as e:
    print(f"error:{e}")
