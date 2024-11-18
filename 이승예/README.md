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
   <td>D0</td>
   <td>D2</td>
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
   <td>GPIO18</td>
 </tr>
</table>

# 네오픽셀 LED 설치
```
$ sudo apt-get update
$ sudo apt-get install gcc make build-essential python3-dev git scons swig

# 사운드 모듈이 비활성화(네오픽셀 충돌 방지)
$ sudo nano /etc/modprobe.d/snd-blacklist.conf
	# 입력 : blacklist snd_bcm2835
	# 저장 : Ctrl+x


# 설정 파일 수정
$ sudo vim /boot/config.txt
	# 맨 아래에 추가:
	   hdmi_force_hotplug=1
	   hdmi_force_edid_audio=1
           dtparam=spi=on
           dtparam=audio=off

#라이브러리 설치
$ git clone https://github.com/jgarff/rpi_ws281x
$ cd rpi_ws281x
$ sudo scons

$ git clone https://github.com/rpi-ws281x/rpi-ws281x-python
$ cd rpi-ws281x-python
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

