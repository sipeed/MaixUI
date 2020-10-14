from machine import I2C
import nes, lcd, sys, time
from sound import CubeAudio
from fpioa_manager import fm
from Maix import FPIOA, GPIO

i2c = I2C(I2C.I2C3, freq=500*1000, sda=27, scl=24)
CubeAudio.init(i2c)
tmp = CubeAudio.check()
print(tmp)

CubeAudio.ready(volume=100)

fm.register(13,fm.fpioa.I2S0_MCLK, force=True)
fm.register(21,fm.fpioa.I2S0_SCLK, force=True)
fm.register(18,fm.fpioa.I2S0_WS, force=True)
fm.register(35,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(34,fm.fpioa.I2S0_OUT_D2, force=True)

import video
v = video.open("/sd/badapple_320_240_15fps.avi")
print(v)
v.volume(90)
while True:
    if v.play() == 0:
        print("play end")
        break
