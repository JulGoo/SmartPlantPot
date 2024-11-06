# 사진 촬영
$sudo apt install fswebcam  
$fswebcam [이름].jpg

# 사진 및 동영상 촬영
$sudo apt install guvcview  
$guvcview

# influxDB 설치

wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update && sudo apt-get install influxdb -y

sudo service influxdb start

sudo service influxdb status


# influxDB 데이터베이스 만들기

$ influx
>create database SmartPlantPot  
>USE SmartPlantPot

### 테이블
식물ID (Plant ID)   
토양 습도 (Soil Moisture)   
물탱크 양 (Water Tank Level)   
온도 (Temperature)   
습도 (Humidity)   
일조량 (Light Exposure)   
식물 이미지 (Plant Image)   
데이터 수집 시간 (Timestamp)   
식물 상태 (Plant Status)   
임계값 (threshold)   

