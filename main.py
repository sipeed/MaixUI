
from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

test_pin=16
fm.fpioa.set_function(test_pin,FPIOA.GPIO7)
test_gpio=GPIO(GPIO.GPIO7,GPIO.PULL_UP)
lcd.init(color=(255,0,0))
lcd.draw_string(lcd.width()//2-68,lcd.height()//2-24, "Welcome to MaixPy", lcd.WHITE, lcd.RED)
v = sys.implementation.version
lcd.draw_string(lcd.width()//2-70,lcd.height()//2+12, 'V{}.{}.{} : maixpy.io'.format(v[0],v[1],v[2]), lcd.WHITE, lcd.RED)
del v
if test_gpio.value() == 0:
    print('PIN 16 pulled down, enter test mode')
    lcd.clear(lcd.PINK)
    lcd.draw_string(lcd.width()//2-68,lcd.height()//2-4, "Test Mode, wait ...", lcd.WHITE, lcd.PINK)
    import sensor
    import image
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)
    lcd.freq(16000000)
    while True:
        img=sensor.snapshot()
        lcd.display(img)
