import cv2
import os
import glob

def create_video_from_photos() -> cv2.VideoWriter:
    photo_directory = '/home/pi/SmartPlantPot/plant_images'

    print("비디오 생성 시작...")

    # 이미지 파일 가져오기
    photos = glob.glob(os.path.join(photo_directory, '*.jpg'))
    photos.sort()

    if not photos:
        print("사진이 없습니다.")
        return None

    print(f"찾은 사진: {photos}")

    first_frame = cv2.imread(photos[0])
    if first_frame is None:
        print("첫 번째 사진을 읽을 수 없습니다.")
        return None

    height, width, layers = first_frame.shape
    video = cv2.VideoWriter(cv2.CAP_FFMPEG, cv2.VideoWriter_fourcc(*'mp4v'), 0.5, (width, height))

    for photo in photos:
        print(f"사진 읽기: {photo}")
        frame = cv2.imread(photo)
        if frame is None:
            print(f"사진을 읽을 수 없습니다: {photo}")
            continue

        frame_resized = cv2.resize(frame, (width, height))
        print(f"{photo} 크기: {frame.shape} -> 리사이즈: {frame_resized.shape}")

        video.write(frame_resized)
        print(f"{photo} 추가됨.")

    # 비디오 객체 반환
    print("비디오 생성 완료.")
    return video


if __name__ == "__main__":
    try:
        video = create_video_from_photos()
        if video:
            print("비디오 생성 완료")
        else:
            print("비디오 생성 실패")
    except Exception as e:
        print(f"오류: {e}")
