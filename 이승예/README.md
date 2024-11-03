### <일조량 분석 및 식물 생장 LED 자동 제어>

## 조도센서 아두이노 측정방법 
```
  <get_lux_arduino.ino>
  //아날로그 값 읽기
  int sensorValue = analogRead(sensorPin);
  //전압으로 변환
  float voltage = sensorValue * (5.0 / 1023.0);
  //lux 값 계산
  float lux = voltage * 500;
```

## 조도센서 라즈베리파이 처리 방법
```
import serial

ser = serial.Serial('/dev/ttyACM0',9600)

while True:
    if ser.in_waiting > 0:
        lux_value = ser.readline().decode('utf-8').strip()
        print(lux_value)
```

## 테스트 측정
 ### 장소
- 방 전등 켰을 때 : 200~400
- 손으로 가렸을 시 : 1000~1300
지속 측정 예정

