import time
import board
import adafruit_bh1750

i2c = board.I2C()  # uses board.SCL and board.SDA


# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_bh1750.BH1750(i2c)
sensor2 = adafruit_bh1750.BH1750(i2c, address=0x5c)

while True:
    print("Sensor 1: %.2f Lux" % sensor.lux)
    print("Sensor 2: %.2f Lux" % sensor2.lux)
    time.sleep(1)
