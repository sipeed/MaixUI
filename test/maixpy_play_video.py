from Maix import GPIO, I2S
from fpioa_manager import fm
import lcd, video, time

lcd.init()

# AUDIO_PA_EN_PIN = None  # Bit Dock and old MaixGo
# AUDIO_PA_EN_PIN = 32      # Maix Go(version 2.20)
AUDIO_PA_EN_PIN = 2     # Maixduino

# open audio PA
if AUDIO_PA_EN_PIN:
    fm.fpioa.set_function(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1)
    wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
    wifi_en.value(1)

# init i2s(i2s0)
i2s = I2S(I2S.DEVICE_0)

# config i2s according to audio info
i2s.channel_config(i2s.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)

fm.fpioa.set_function(34, fm.fpioa.I2S0_OUT_D1)
fm.fpioa.set_function(35, fm.fpioa.I2S0_SCLK)
fm.fpioa.set_function(33, fm.fpioa.I2S0_WS)

v = video.open("/sd/badapple_320_240_15fps.avi")
print(v)
v.volume(50)
while True:
    if v.play() == 0:
        print("play end")
        break
v.__del__()
