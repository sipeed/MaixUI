# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from fpioa_manager import fm
from Maix import FPIOA, GPIO
from Maix import GPIO, I2S
from fpioa_manager import fm
import lcd, nes, time

lcd.init()

# AUDIO_PA_EN_PIN = None  # Bit Dock and old MaixGo
# AUDIO_PA_EN_PIN = 32      # Maix Go(version 2.20)
AUDIO_PA_EN_PIN = 2     # Maixduino

# open audio PA
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
    wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
    wifi_en.value(1)

# init i2s(i2s0)
i2s = I2S(I2S.DEVICE_0)

# config i2s according to audio info
i2s.channel_config(i2s.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)

fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
fm.register(33, fm.fpioa.I2S0_WS, force=True)

lcd.init(freq=15000000)
lcd.register(0x36, 0x68)

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
        state = 1
        nes.loop()
        nes.input(state | 128, 0, 0)
        nes.loop()

    finally:
      nes.free()
