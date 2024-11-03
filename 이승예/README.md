### <일조량 분석 및 식물 생장 LED 자동 제어>


```
  ## Arduino
  //아날로그 값 읽기
  int sensorValue = analogRead(sensorPin);
  //전압으로 변환
  float voltage = sensorValue * (5.0 / 1023.0);
  //lux 값 계산
  float lux = voltage * 500;
```

## 테스트 측정
# 장소
- 방 전등 켰을 때 : 200~400
- 손으로 가렸을 시 : 1000~1300
지속 측정 예정
