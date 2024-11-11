import cv2
import os
import glob
from datetime import datetime, timedelta
from influxdb import InfluxDBClient

def create_video_from_photos(start_date, end_date, output_filename):

    client = InfluxDBClient(host='', port=8086, username='', password='', database='')

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
    video = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'), 0.5, (width, height))


    for photo in sorted(photos):
        print(f"read photo:{photo}")
        frame = cv2.imread(photo)
        if frame is None:
            print(f"no frame : {photo}")
            continue
 
        frame_resized = cv2.resize(frame, (width, height))
        print(f"{photo} size : {frame.shape} -> resize : {frame_resized.shape}")

        video.write(frame_resized)
        print(f"{photo} add.")

        json_body = [
             {
                 "measurement":"timelapses",
                 "tags":{
                     "start_date": start_date.strftime('%Y-%m-%d'),
                     "end_date": end_date.strftime('%Y-%m-%d'),
                     "file_name": output_filename,
                     },
                     "fields":{
                         "created_at":int(datetime.now().timestamp())
                        }
                     }
                ]
    client.write_points(json_body)

    video.release()
    print(f"{output_filename} make ok. file size : {os.path.getsize(output_filename)} bytes")


start_date = input("start(YYYY-MM-DD): ")
end_date = input("end(YYYY-MM-DD): ")
output_filename = input("filename ex)timelapse.mp4): ")

output_filepath = os.path.join('/home/pi/timelapse', output_filename)

try:
    create_video_from_photos(start_date, end_date, output_filepath)
except Exception as e:
    print(f"error:{e}")
