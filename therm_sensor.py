import w1thermsensor
import sys

sensor = w1thermsensor.W1ThermSensor()
temp = sensor.get_temperature()
sys.exit(temp)

