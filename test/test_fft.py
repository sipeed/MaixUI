from Maix import GPIO, I2S, FFT
import image, lcd, math
from board import board_info
from fpioa_manager import fm

#from sound import CubeAudio
from es8374 import ES8374

sample_rate = 44100
sample_points = 1024
fft_points = 512
hist_x_num = 240

lcd.init(freq=15000000)

fm.register(19,fm.fpioa.I2S0_MCLK, force=True)
fm.register(35,fm.fpioa.I2S0_SCLK, force=True)
fm.register(33,fm.fpioa.I2S0_WS, force=True)
fm.register(34,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(18,fm.fpioa.I2S0_OUT_D2, force=True)

es8374_dev = ES8374()

# init i2s(i2s0)
i2s = I2S(I2S.DEVICE_0, pll2=262144000, mclk=31)

# config i2s according to audio info # STANDARD_MODE LEFT_JUSTIFYING_MODE RIGHT_JUSTIFYING_MODE
i2s.channel_config(I2S.CHANNEL_0, I2S.RECEIVER, resolution=I2S.RESOLUTION_16_BIT, cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)

i2s.set_sample_rate(sample_rate)

img = image.Image(size=(240, 240))
hist_width = int(240 / hist_x_num)#changeable
x_shift = 0
while True:
    audio = i2s.record(sample_points)
    fft_res = FFT.run(audio.to_bytes(), fft_points)
    fft_amp = FFT.amplitude(fft_res)
    #print(fft_amp)
    img = img.clear()
    x_shift = 0
    for i in range(hist_x_num):
        hist_height = 240 if fft_amp[i] > 240 else fft_amp[i]
        img = img.draw_rectangle((x_shift, 10, hist_width, hist_height), [255,255,255], 1,True)
        #print((x_shift, 0, hist_width, hist_height))
        x_shift = x_shift + hist_width
    lcd.display(img)
    fft_amp.clear()

