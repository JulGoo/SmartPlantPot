# 통합코드

### 파일구조
```
/home/pi/SmartPlantPot/
│
├──arduino/
│  └──main.ino (아두이노 실행 파일)
│
├──modules/
│  ├──각 모듈 .py파일
│  └──...
│
├──plant_images/
│  ├──식물 이미지.jpg
│  └──...
│
├──timelapse/
│  └──타임랩스 영상.mp4
│
├──threshold/
│  └──threshold.txt (임계값 정의 텍스트 파일)
│
└──main.py
```

### `Main.py`
- 각 기능을 하는 py파일들을 MultiThread로 병령 실행
- 아두이노 Serial 포트를 여러 파일에서 사용하면 오류가 발생
  - 각 py파일의 Serial 데이터를 가져오는 로직 제거
  - 해당 파일에서만 Serial 데이터를 읽어 Queue에 데이터를 담아 각 스레드(py파일)로 전달

<br>

- 통합 아두이노 파일에서 출력한 Serial 데이터 파싱
  ```
  # Serial: 토양습도값,초음파거리값,조도값,온도값,습도값
  parts = line.split(',')
  ```

- ex) Queue에 데이터 넣기 
  ```
  queue.put(('soil_moisture_value', int(parts[0]))) # 첫 번째 값: 토양 습도
  queue.put(('water_tank_value', int(parts[1])))    # 두 번째 값: 물탱크 거리
  parts[2]
  parts[3]
  parts[4]
  ⁝
  ```
- ex) 스레드 실행
  ```
  # 자신의 py파일에서 main함수를 import
  from soil_moisture_control import monitor_and_control_soil_moisture
  ⁝
  soil_moisture_thread = threading.Thread(target=monitor_and_control_soil_moisture, args=(queue,), daemon=True)
  soil_moisture_thread.start()
  soil_moisture_thread.join()
  ```
- ex) 각 py파일에서 필요 데이터 추출하기
  ```
  def monitor_and_control_soil_moisture(queue):
    while True:
          if not queue.empty():            
              # 큐에서 토양 습도 데이터 받기
              data_type, value = queue.get()
              if data_type == 'soil_moisture_value':
                  soil_moisture = value
  ```


---
