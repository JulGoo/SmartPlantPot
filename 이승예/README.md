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
  int lux = static_cast<int>((5.0 - voltage) * 50);
```

## 주요 기능

- 자동/수동 LED 조명 제어
- 실시간 조도 모니터링
- 조도 데이터 InfluxDB 저장
- 주간/야간 시간대별 동작 제어
- 조도 부족 시 알림 기능

## 시스템 구조

### 1. 초기화 및 설정
```python
# LED 설정
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# InfluxDB 연결 설정
client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='spp')

# 밝기 프리셋 정의 (0-255 범위)
BRIGHTNESS_PRESETS = {
    25: 64,   # 25% = 64 (255 * 0.25)
    50: 128,  # 50% = 128 (255 * 0.50)
    75: 191,  # 75% = 191 (255 * 0.75)
    100: 255  # 100% = 255 (255 * 1.00)
}

# 주간시간 설정
DAYTIME_START = 6  # 오전 6시
DAYTIME_END = 18   # 오후 6시
```

### 2. LED 제어 시스템

#### 수동 제어 모드
- 사전 정의된 밝기 프리셋으로 LED 제어 가능 (25%, 50%, 75%, 100%)
- LED ON/OFF 기능
- 조도 부족 시 알림 발송

```python
def turn_on_led_with_brightness(brightness_percent):
    global manual_control
    try:
        manual_control = True
        brightness = BRIGHTNESS_PRESETS[brightness_percent]
        neo.clear_strip()
        neo.fill_strip(brightness, brightness, brightness)
        neo.update_strip()
        return True
    except Exception as e:
        print(f"light_control_system.py: 수동 LED ON 실패: ", e)
        return False
```

#### 자동 제어 모드
- 주간 시간대(06:00-18:00)에만 작동
- 현재 조도가 설정된 임계값보다 낮을 경우 자동으로 LED 밝기 조절
- 10분 간격으로 조도 체크 및 제어

```python
def calculate_led_brightness(current_lux):
    light_threshold = get_light_threshold()

    if current_lux >= light_threshold:
        return 0

    # 부족한 조도량 계산 (lux 단위)
    lux_deficit = light_threshold - current_lux
    
    # LED 밝기값 당 발생하는 lux 값 (실험 측정치)
    LUX_PER_BRIGHTNESS = 0.5

    required_brightness = int(lux_deficit / LUX_PER_BRIGHTNESS)
    return min(required_brightness, 255)
```


### 3. 데이터 관리
- 조도 데이터 실시간 InfluxDB 저장
- 측정 시간 및 조도값(lux) 기록
- 조도 임계값 설정 파일 관리
