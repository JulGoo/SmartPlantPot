# 사진 촬영
$ python capture.py  

# 타임랩스
$ python timelapse.py

# OpenCV 라이브러리 설치
wget https://github.com/Qengineering/Install-OpenCV-Raspberry-Pi-64-bits/raw/main/OpenCV-4-10-0.sh
sudo chmod 755 ./OpenCV-4-10-0.sh
./OpenCV-4-10-0.sh

$ sudo apt-get update
$ sudo apt-get upgrade
sudo apt-get install build-essential cmake git unzip pkg-config
sudo apt-get install libjpeg-dev libpng-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install libgtk2.0-dev libcanberra-gtk* libgtk-3-dev
sudo apt-get install libgstreamer1.0-dev gstreamer1.0-gtk3
sudo apt-get install libgstreamer-plugins-base1.0-dev gstreamer1.0-gl
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install python3-dev python3-numpy python3-pip
sudo apt-get install libtbbmalloc2 libtbb-dev
sudo apt-get install libv4l-dev v4l-utils
sudo apt-get install libopenblas-dev libatlas-base-dev libblas-dev
sudo apt-get install liblapack-dev gfortran libhdf5-dev
sudo apt-get install libprotobuf-dev libgoogle-glog-dev libgflags-dev
sudo apt-get install protobuf-compiler

## Swap 설정
$ sudo vim /sbin/dphys-swapfile   CONF_MAXSWAP = 2048  -> CONF_MAXSWAP = 4096
$ sudo vim /etc/dphys-swapfile   CONF_SWAPSIZE = 200 -> CONF_SWAPSIZE = 4096
$ sudo reboot

# influxDB 설치
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update && sudo apt-get install influxdb -y
sudo service influxdb start
sudo service influxdb status  

