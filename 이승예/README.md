### <일조량 분석 및 식물 생장 LED 자동 제어>

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
   <td>A0</td>
   <td>A0</td>
 </tr>
</table>


## 라즈베리파이와 네오픽셀 LED 핀 연결도
<table>
 <tr>
   <th>LED 핀</th>
   <th>라즈베리파이 핀</th>
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
   <td>GPIO10</td>
 </tr>
</table>

# Pi5 Neo (네오픽셀 라이브러리)
```
$sudo raspi-config
   Interface Options 선택
   SPI 선택
   Yes 선택하여 활성화
   Finish 선택

$sudo pip3 install pi5neo 
   오류(error : externally-managed-environment ==> sudo pip3 install pi5neo --break-system-packages)

$sudo reboot

(파일 실행 후 권한 에러 뜨면)
# 사용자를 spi 그룹에 추가
sudo usermod -a -G spi,gpio pi

# SPI 장치 권한 설정
sudo chown root:spi /dev/spidev0.0
sudo chmod 660 /dev/spidev0.0

# 변경사항 적용을 위한 재부팅
sudo reboot
```

## 조도센서 아두이노 측정방법 
```
  <light_sensor.ino>
  //아날로그 값 읽기
  int sensorValue = analogRead(luxPin);
  //전압으로 변환
  float voltage = sensorValue * (5.0 / 1023.0);
  //lux 값 계산
  int lux = (5.0 - voltage) * 2000;
```

## 조도값 기록 / LED 제어 (light_control_system)
- def
   - monitor_and_control_light(queue): 조도 모니터링 및 LED 제어
   - get_hourly_average(): 최근 1시간 평균 조도 계산
   - calculate_led_brightness(current_lux): LED 밝기 계산
   - control_leds(strip, brightness): LED 밝기 제어

- InfluxDB
   - measurement: Light_Exposure
   - fields: lux

