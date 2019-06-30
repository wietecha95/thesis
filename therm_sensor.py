import w1thermsensor

sensor = w1thermsensor.W1ThermSensor()

while True:
    temp = sensor.get_temperature()
    print(temp)
