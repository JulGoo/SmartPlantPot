# 토양 습도 및 수분 공급 분석

### 사용 센서 및 부품
| 역할     | 연결                           | 센서/부품                     |
|----------|-------------------------------|-------------------------------|
| 입력     | 아두이노                       | 토양 습도 센서, 초음파 센서 (HC-SR04) |
| 출력     | 라즈베리파이                   | 수중 모터                     |

### 진행 내용
<div style="display: flex; align-items: center;">
    <img src="https://static-00.iconduck.com/assets.00/apps-arduino-icon-2048x2048-42m5bo99.png" alt="ino" width="20" height="20" style="margin-right: 10px;">
    <h4>아두이노 (SoilMoistureAndUltrasonicSensor.ino)</h4>
</div>

- 토양 습도 센서의 토양 습도 아날로그 값 측정
- 초음파 센서의 물탱크 수위 값 측정 및 오차적용
    ```
    // Echo 핀에서 반사파 수신 및 시간 측정
    duration = pulseIn(echoPin, HIGH);

    // 거리를 센티미터로 변환
    distance = duration * 0.034 /2;

    // 실제 초음파 센서 거리 오차 적용(+1cm)
    distance += 1;
    ```

<br>
<div style="display: flex; align-items: center;">
    <img src="https://cdn.iconscout.com/icon/free/png-256/free-python-3521655-2945099.png?f=webp" alt="py" width="20" height="20" style="margin-right: 10px;">
    <h4>라즈베리파이 Python (soil_moisture_water_tank_moniter.py)</h4>
</div>

- 아두이노와 연동하여 Serial 데이터 읽고 파싱
- 실시간 토양 습도 값과 설정 임계값에 따른 모터 작동
- InfluxDB에 데이터 저장(토양 습도 값, 물 탱크 수위)
    ```
    # 토양 습도
    "measurement": "soil_moisture",
    "fields": {
        "soil_moisture": soil_moisture,
    }
    ```
    ```
    # 물 탱크 수위
    "measurement": "water_tank_distance",
    "fields": {
        "water_tank_distance": distance
    }
    ```
    

<br>

---
