# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import nes, lcd

#lcd.register(0x36, 0x20)

import sys, time

from fpioa_manager import fm
from Maix import FPIOA, GPIO
from machine import I2C
from sound import CubeAudio
i2c = I2C(I2C.I2C3, freq=600*1000, sda=31, scl=30)
CubeAudio.init(i2c)
tmp = CubeAudio.check()
print(tmp)
# cube
fm.register(19,fm.fpioa.I2S0_MCLK, force=True)
fm.register(35,fm.fpioa.I2S0_SCLK, force=True)
fm.register(33,fm.fpioa.I2S0_WS, force=True)
fm.register(34,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(18,fm.fpioa.I2S0_OUT_D2, force=True)

CubeAudio.ready()
CubeAudio.i2s.set_sample_rate(44100)

lcd.init(freq=15000000)
lcd.register(0x36, 0x68)

from button import button_io, sipeed_button

tmp = sipeed_button()
#button_io.config(23, 31, 20) # amigo
button_io.config(10, 16, 11) # cube

if __name__ == "__main__":

    # B A SEL START UP DOWN LEFT RIGHT
    # 1 2 4   8     16  32   64   128
    state = 0

    try:
      nes.init(nes.INPUT)
      nes.load("mario.nes")
      for i in range(20000):
        nes.loop()
      for i in range(2000):
        nes.loop()
        nes.input(8, 0, 0)
        nes.loop()
        nes.input(0, 0, 0)
      nes.loop()
      nes.input(8, 0, 0)
      nes.loop()
      nes.input(0, 0, 0)
      while True:
        #print(time.ticks_ms())
        nes.loop()
        state = 0
        nes.loop()
        if button_io.home_button.value() == 0:
          nes.loop()
          state = state | 1
          nes.loop()
        if button_io.back_button.value() == 0:
          nes.loop()
          state = state | 64
          nes.loop()
        if button_io.next_button.value() == 0:
          nes.loop()
          state = state | 128
          nes.loop()
        nes.input(state, 0, 0)
        nes.loop()

    finally:
      nes.free()
