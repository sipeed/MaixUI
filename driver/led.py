
from fpioa_manager import *
from Maix import FPIOA, GPIO

fm.register(13, fm.fpioa.GPIOHS13)
fm.register(12, fm.fpioa.GPIOHS12)
fm.register(14, fm.fpioa.GPIOHS14)
fm.register(32, fm.fpioa.GPIOHS3)

class cube_led:

    r = GPIO(GPIO.GPIOHS13, GPIO.OUT)
    g = GPIO(GPIO.GPIOHS12, GPIO.OUT)
    b = GPIO(GPIO.GPIOHS14, GPIO.OUT)
    w = GPIO(GPIO.GPIOHS3, GPIO.OUT)

    def init():
        cube_led.r.value(1)
        cube_led.g.value(1)
        cube_led.b.value(1)
        cube_led.w.value(1)

    def unit_test():
        import time
        cube_led.r.value(0)
        time.sleep(1)
        cube_led.r.value(1)
        cube_led.g.value(0)
        time.sleep(1)
        cube_led.g.value(1)
        cube_led.b.value(0)
        time.sleep(1)
        cube_led.b.value(1)
        cube_led.w.value(0)
        time.sleep(1)
        cube_led.w.value(1)

cube_led.init()

if __name__ == "__main__":

    cube_led.unit_test()

