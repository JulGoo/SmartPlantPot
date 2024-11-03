import serial

ser = serial.Serial('/dev/ttyACM0',9600)

while True:
    if ser.in_waiting > 0:
        lux_value = ser.readline().decode('utf-8').strip()
        print(lux_value)
