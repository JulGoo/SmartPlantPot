### <일조량 분석 및 식물 생장 LED 자동 제어>
<br>
<br>

## 아두이노와 조도센서 핀 연결도
<table>
 <tr>
   <th>센서 핀</th>
   <th>아두이노 핀</th>
 </tr>
 <tr>
   <td>VCC</td>
   <td>5V</td>
 </tr>
 <tr>
   <td>GND</td>
   <td>GND</td>
 </tr>
 <tr>
   <td>D0</td>
   <td>D2</td>
 </tr>
 <tr>
   <td>A0</td>
   <td>A0</td>
 </tr>
</table>


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
- 방 전등 켰을 때 : 700~800 (lux)
- 손으로 가렸을 시 : 2000~2400 (lux)<br/>
지속 측정 예정

