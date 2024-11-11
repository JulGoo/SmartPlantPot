# 사진 촬영
$ python capture.py  

## 설명
- 웹캠을 이용한 사진 촬영  
- 현재 날짜와 시간으로 파일 생성  
- 4시간(14400초) 간격으로 사진 촬영  
- 웹캠 연결 필수, $lsusb로 연결 유무 확인 가능 

## 요구사항
- python
- $pip install opencv-python 

# 타임랩스 촬영
$ python timelapse.py

## 설명
- 특정 날짜 범위에 해당하는 사진 검색
- 사진을 읽고, 크기를 조정하여 비디오로 변환
- 생성된 비디오 파일 저장

## 요구사항
- python
- $ pip install opencv-python

## 사용 방법
- 스크립트 실행 후 시작 날짜와 종료 날짜와 파일명을 입력합니다.
- 파일명의 경우 꼭 확장자(.mp4)를 추가해야만 합니다.
