import cv2
import os
import glob

# video_lenth 동영상 길이(초)
def create_video_from_photos(video_lenth:int = 10):
    photo_directory = './plant_images'

    # 이미지 파일 가져오기
    photos = glob.glob(os.path.join(photo_directory, '*.jpg'))
    photos.sort()

    if not photos:
        print("timelapse.py: 이미지가 존재하지 않습니다.")
        return None

    # 첫 번째 이미지 읽기(프레임 생성)
    first_frame = cv2.imread(photos[0])
    if first_frame is None:
        print("timelapse.py: 이미지를 읽을 수 없습니다.")
        return None

    height, width, layers = first_frame.shape

    # 비디오 파일 저장 경로 지정
    video_path = './timelapse/timelapse.mp4'

    # 기존 파일이 존재하면 삭제
    if os.path.exists(video_path):
        os.remove(video_path)

    # FPS 계산(이미지 수 / 비디오 길이)
    fps = photos.__len__() / video_lenth

    # 비디오 객체 생성
    video_writer = cv2.VideoWriter(
        video_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    # 이미지 전체를 비디오 객체에 추가
    for photo in photos:
        frame = cv2.imread(photo)
        if frame is None:
            continue

        frame_resized = cv2.resize(frame, (width, height))
        video_writer.write(frame_resized)

    video_writer.release()
    print(f"timelapse.py: 비디오 생성 완료. 파일 경로: {video_path}")
    return video_path  # 비디오 파일 경로 반환
