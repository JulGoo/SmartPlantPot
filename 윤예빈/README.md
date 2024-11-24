# 온습도 분석 및 데이터 시각화



## 온습도 분석

### 요구사항
- DHT sensor library 설치 (install all)

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

### 요구사항
- pip install pandas
- pip install matplotlib

### 사용자에게 기간 입력 받기
```
    # 기간별 쿼리 조건
    if period == "7d":
        time_filter = "WHERE time > now() - 7d"
    elif period == "30d":
        time_filter = "WHERE time > now() - 30d"
    elif period == "1y":
        time_filter = "WHERE time > now() - 365d"  # influxDB에서 1y를 인식하지 못함 -> 365d
    elif period == "all":
        time_filter = ""
    else:
        raise ValueError("Invalid period. Use '7d', '30d', '1y', or 'all'.")
```

### 이미지 저장
io.BytesIO 객체로 메모리에 저장

저장된 이미지 텔레그램으로 전송하기
```
import telegram

bot = telegram.Bot(token="YOUR_BOT_TOKEN")
chat_id = "USER_CHAT_ID"

image = main()
bot.send_photo(chat_id=chat_id, photo=image)
```


