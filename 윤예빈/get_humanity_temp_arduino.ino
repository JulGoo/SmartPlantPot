#include <DHT.h>  // DHT 센서 사용을 위한 라이브러리

DHT dht(6, DHT22);  // 6번 핀에 DHT22 센서 연결

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();  // 습도 값
  float t = dht.readTemperature();  // 온도 값

  Serial.print(h);  // 습도 데이터
  Serial.print(",");  // 구분자
  Serial.println(t);  // 온도 데이터

  delay(1000);  // 1초 간격으로 측정
}
