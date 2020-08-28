
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
fm.register(20, fm.fpioa.GPIO5, force=True)
cs = GPIO(GPIO.GPIO5, GPIO.OUT)
#cs.value(0)
#utime.sleep_ms(2000)

print(os.listdir())
spi = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=400*1000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=21, mosi=8, miso=15)#使用程序配置了 cs0 则无法读取 W25QXX
print(os.listdir())
print(spi)

while True:
    fm.register(21, fm.fpioa.SPI1_SCLK, force=True)
    fm.register(8, fm.fpioa.SPI1_D0, force=True)
    fm.register(15, fm.fpioa.SPI1_D1, force=True)
    cs.value(0)
    write_data = bytearray([0x90, 0x00, 0x00, 0x00])
    spi.write(write_data)
    id_buf = bytearray(2)
    spi.readinto(id_buf, write=0xff)
    print(id_buf)
    print(time.ticks_ms())
    cs.value(1)
    #cs.value(0)
    utime.sleep_ms(200)
    #utime.sleep_ms(2200)
    fm.register(27, fm.fpioa.SPI1_SCLK, force=True)
    fm.register(28, fm.fpioa.SPI1_D0, force=True)
    fm.register(26, fm.fpioa.SPI1_D1, force=True)
    print(os.listdir())

spi.deinit()
