import MySQLdb
import time
from DFRobot_MAX17043 import DFRobot_MAX17043
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import w1thermsensor

print("Establishing connection.")
print("Connection established")
curs =db.cursor()
gauge = DFRobot_MAX17043()


def interruptCallBack(channel):
  gauge.clearInterrupt()
  print('Low power alert interrupt!')
  #put your battery low power alert interrupt service routine here

def init_soc():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.IN)
    GPIO.add_event_detect(8, GPIO.FALLING, callback = interruptCallBack, bouncetime = 5)
    rslt = gauge.begin()
    while rslt != 0:
      print('gauge begin faild')
      time.sleep(2)
      rslt = gauge.begin()
    gauge.setInterrupt(32) #use this to modify alert threshold as 1% - 32% (integer)
    print('gauge begin successful')


def init_ads():
    # Software SPI configuration:
    CLK  = 18
    MISO = 23
    MOSI = 24
    CS   = 25
    # mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
    # Hardware SPI configuration:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    return mcp


def insert_data(u, soc, temp, intensity, intensity_uv):
    try:
        command = 'insert into bat (U, SOC, TEMP, INTENSITY, INTENSITY_UV) values({}, {}, {}, {}, {})'.format(u, soc, temp, intensity, intensity_uv)
        print(command)
        curs.execute(command)
        db.commit()
    except Exception as e:
        print("Can't insert record")
        print(e)


def main():
    init_soc()
    mcp = init_ads()
    sensor = w1thermsensor.W1ThermSensor()
    print("Everything is properly configured!")
    while True:
        time.sleep(2)
        UV = 0
        INTENSITY = 2
        values = [0]*8
        for i in range(8):
            values[i] = mcp.read_adc(i)
        insert_data(gauge.readVoltage(), gauge.readPercentage(), sensor.get_temperature(), values[INTENSITY], values[UV])


main()
