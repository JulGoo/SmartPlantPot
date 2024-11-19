#include <DHT.h>

// 핀 설정
const int soilMoisturePin = A0; // 토양 습도 센서
const int trigPin = 9;  // 초음파 센서 Trig 핀
const int echoPin = 10; // 초음파 센서 Echo 핀
const int luxPin = A1; // 조도 센서
const int DHTPin = 2; // DHT 센서

// DHT 센서 설정
DHT dht(DHTPin, DHT11);

// 변수 선언
long duration;
int distance;
int soilMoistureValue;
int lightSensorValue;
int temperatureValue;
int humidityValue;

void setup() {
  // 시리얼 통신 시작
  Serial.begin(9600);

  // 핀 모드 설정
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(soilMoisturePin, INPUT);
  pinMode(luxPin, INPUT);

  // DHT 센서 시작
  dht.begin();
}

// 토양 습도 측정
int soilMoisture() {
  int sensorValue = analogRead(soilMoisturePin);
  return sensorValue;
}

// 초음파 센서 거리 측정
int ultrasonic() {
  // Trig 핀에 HIGH 신호를 10 마이크로초 동안 송신
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Echo 핀에서 반사파 수신 및 시간 측정
  duration = pulseIn(echoPin, HIGH);
  // 거리를 센티미터로 변환
  distance = duration * 0.034 / 2;
  // 실제 초음파 센서 거리 오차 적용(+1cm)
  distance += 1;
  return distance;
}

// 온도 측정
int temperature() {
  float temp = dht.readTemperature();
  return static_cast<int>(temp);
}

// 습도 측정
int humidity() {
  float hum = dht.readHumidity();
  return static_cast<int>(hum);
}

// 조도 측정
int lightSensor() {
  // 조도 측정
  int sensorValue = analogRead(luxPin);
  // 전압으로 변환
  float voltage = sensorValue * (5.0 / 1023.0);
  // lux 값 계산
  int lux = static_cast<int>((5.0 - voltage) * 2000);
  return lux;
}

void loop() {
  soilMoistureValue = soilMoisture();
  distance = ultrasonic();
  lightSensorValue = lightSensor();
  temperatureValue = temperature();
  humidityValue = humidity();

  Serial.print(soilMoistureValue);
  Serial.print(",");
  Serial.print(distance);
  Serial.print(",");
  Serial.print(lightSensorValue);
  Serial.print(",");
  Serial.print(temperatureValue);
  Serial.print(",");
  Serial.println(humidityValue);

  delay(1000);  // 1초 대기
}