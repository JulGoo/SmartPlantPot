# 온습도 분석 및 데이터 시각화



## 온습도 분석

arduino 스케치 -> 라이브러리 포함하기 -> 라이브러리 관리

DHT sensor library 설치 (install all)

### 아두이노와 온습도센서(DHT22) 핀 연결도

|DHT22|아두이노|
|---|---|
|VCC|5V|
|D0|D6|
|GND|GND|

### 온습도센서(DHT22) 아두이노 측정 방법 (get_humidity_temperature_arduino.ino)
- DHT 센서를 위한 라이브러리 사용

```
#include <DHT.h>  // DHT 센서 사용을 위한 라이브러리

...

float h = dht.readHumidity();  // 습도 값 도출
float t = dht.readTemperature();  // 온도 값 도출
```

### 온습도 데이터 InfluxDB 저장
- 습도
  - measurement : Humidity
  - fields : Humjidity
  
- 온도
  - measurement : Temperature
  - fields : Temperature

## 데이터 시각화
