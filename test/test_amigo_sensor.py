# Hello World Example
#
# Welcome to the MaixPy IDE!
# 1. Conenct board to computer
# 2. Select board at the top of MaixPy IDE: `tools->Select Board`
# 3. Click the connect buttion below to connect board
# 4. Click on the green run arrow button below to run the script!

import sensor, image, time, lcd
# -*- coding: UTF-8 -*-
# Untitled - By: Echo - 周五 4月 2 2020
# start of pmu_axp173.py
from machine import I2C, Timer
import lcd, utime
from fpioa_manager import fm
from Maix import GPIO
import sensor, image, time

class AXP173:
    class PMUError(Exception):
        pass
    class OutOfRange(PMUError):
        pass
    def __init__(self, i2c_dev=None, i2c_addr=0x34):
        from machine import I2C
        if i2c_dev is None:
            try:
                self.i2cDev = I2C(I2C.I2C0, freq=400000, scl=24, sda=27)
            except Exception:
                raise PMUError("Unable to init I2C0 as Master")
        else:
            self.i2cDev = i2c_dev
        self.i2cDev.scan()
        self.axp173Addr = i2c_addr
    def __write_reg(self, reg_address, value):
        self.i2cDev.writeto_mem(
            self.axp173Addr, reg_address, value, mem_size=8)
    def writeREG(self, regaddr, value):
        self.__write_reg(regaddr, value)
# end of pmu_axp173.py

# ------------------------

lcd.init()
i2cDev = I2C(I2C.I2C0, freq=400000, scl=24, sda=27)
print(i2cDev.scan())

axp173 = AXP173()
axp173.writeREG(0x27, 0x20)
axp173.writeREG(0x28, 0x0C)

lcd.init(freq=20000000)

#sensor.reset(choice=2)                      # Reset and initialize the sensor. It will
                                    ## run automatically, call sensor.run(0) to stop
#sensor.set_pixformat(sensor.YUV422) # Set pixel format to RGB565 (or GRAYSCALE)
#sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
##sensor.sleep(1)
#sensor.skip_frames(time = 5000)     # Wait for settings take effect.
#clock = time.clock()                # Create a clock object to track the FPS.

#while(True):
    #clock.tick()                    # Update the FPS clock.
    #img = sensor.snapshot()         # Take a picture and return the image.
    #lcd.display(img)                # Display on LCD
    ## print(clock.fps())              # Note: MaixPy's Cam runs about half as fast when connected
                                    ## to the IDE. The FPS should increase once disconnected.



while True:

    #time.sleep(2)

    try:
        sensor.reset(choice=1)
        sensor.set_pixformat(sensor.YUV422)
        sensor.set_framesize(sensor.QVGA)
        sensor.skip_frames(time=2000)
        for i in range(50):
            img = sensor.snapshot()
            lcd.display(img)
    except Exception as e:
        print(e)

    try:
        sensor.reset(choice=2)
        sensor.set_pixformat(sensor.YUV422)
        sensor.set_framesize(sensor.QVGA)
        sensor.skip_frames(time=2000)
        for i in range(50):
            img = sensor.snapshot()
            lcd.display(img)

    except Exception as e:
        print(e)
