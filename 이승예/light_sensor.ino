const int luxPin = A0;  // 조도 센서

void setup() {
  Serial.begin(9600);
}

void loop() {
  // 조도 측정
  int sensorValue = analogRead(luxPin);
  // 전압으로 변환
  float voltage = sensorValue * (5.0 / 1023.0);
  // lux 값 계산
  int lux = (5.0 - voltage) * 2000;
  
  Serial.println(lux);   // 조도값
  
  delay(600000);  // 10분(600,000ms) 대기
}
