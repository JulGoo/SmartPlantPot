# 토양 습도 및 수분 공급 분석

### 사용 센서 및 부품
| 역할     | 연결                           | 센서/부품                     |
|----------|-------------------------------|-------------------------------|
| 입력     | 아두이노                       | 토양 습도 센서, 초음파 센서 (HC-SR04) |
| 출력     | 라즈베리파이                   | 수중 모터, 모터 드라이브              |

<br/>

### 아두이노, 라즈베리파이 핀 연결도
<table>
 <tr>
   <th>아두이노 핀</th>
   <th>토양 습도 센서</th>
   <th>주파수 거리 센서</th>
 </tr>
 <tr>
   <td>5V</td>
   <td>VCC</td>
   <td>VCC</td>
 </tr>
 <tr>
   <td>GND</td>
   <td>GND</td>
   <td>GND</td>
 </tr>
 <tr>
   <td>A1</td>
   <td>OUT</td>
   <td></td>
 </tr>
 <tr>
   <td>D9</td>
   <td></td>
   <td>TRIG</td>
 </tr>
  <tr>
   <td>D10</td>
   <td></td>
   <td>ECHO</td>
 </tr>
</table>
<table>
 <tr>
   <th>라즈베리파이 핀</th>
   <th>수중 모터 드라이브</th>
 </tr>
 <tr>
   <td>5V</td>
   <td>VCC</td>
 </tr>
 <tr>
   <td>GND</td>
   <td>GND</td>
 </tr>
 <tr>
   <td>GPIO 14</td>
   <td>A-1B</td>
 </tr>
</table>

<br/>

### 진행 내용
**1. 아두이노 (`SoilMoistureAndUltrasonicSensor.ino`)**
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

**2. 토양 습도 기록 / 수중 모터 동작 (`soil_moisture_control`)**
- def
   - `*monitor_and_control_soil_moisture(queue)`: *토양 습도 제어
   - `log_soil_moisture(soil_moisture)`: 토양 습도 값 InfluxDB 기록
   - `activate_water_pump()`: 물 공급

<br>

- InfluxDB
   - measurement: `soil_moisture`
   - fields: `soil_moisture`

<br>

**3. 물 탱크 수위 기록 (`water_tank_monitor`)**
- def
   - `*monitor_and_log_water_tank_level(queue)`: *물탱크 수위 확인 및 기록
   - `get_tank_level_percent(distance_to_water)`: 물탱크 수위 퍼센트 변환
   - `log_water_tank_level(level_percent)`: 물탱크 수위 InfluxDB 기록

<br>

- InfluxDB
   - measurement: `water_tank_level`
   - fields: `level_percent`
    
<br>

---
