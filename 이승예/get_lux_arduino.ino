const int sensorPin = A0;

void setup() {
  Serial.begin(9600);

}

void loop() {
  //아날로그 값 읽기
  int sensorValue = analogRead(sensorPin);
  //전압으로 변환
  float voltage = sensorValue * (5.0 / 1023.0);
  //lux 값 계산
  float lux = voltage * 500;


  Serial.println(lux);

  delay(1000);
}
