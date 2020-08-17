
from machine import SPI
import utime
from Maix import GPIO
from fpioa_manager import fm

# MaixBit       W25QXX
# CS  (25)      CS
# MOSI(22)      D0 DI(MOSI)
# MISO(24)      D1 DO(MISO)
# SCK (23)      SCK

''' CUBE
07 |  V
15 | 21
20 | 08
 G | 06
'''

''' AMIGO
24 |  V
06 | 11
12 | 10
 G | 27
'''

print("Welcome to MicroPython!")
fm.register(12, fm.fpioa.GPIOHS16, force=True)
cs = GPIO(GPIO.GPIOHS16, GPIO.OUT)
#cs.value(0)
#utime.sleep_ms(2000)

spi = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=400*1000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=11, mosi=10, miso=6)#使用程序配置了 cs0 则无法读取 W25QXX

print(spi)

while True:
    cs.value(0)
    write_data = bytearray([0x90, 0x00, 0x00, 0x00])
    spi.write(write_data)
    id_buf = bytearray(2)
    spi.readinto(id_buf, write=0xff)
    print(id_buf)
    print(time.ticks_ms())
    #cs.value(0)
    utime.sleep_ms(200)
    cs.value(1)
    #utime.sleep_ms(2200)

spi.deinit()
