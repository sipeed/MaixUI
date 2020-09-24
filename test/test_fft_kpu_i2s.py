
import sensor, image, time, lcd

from machine import I2C
import lcd, utime
from fpioa_manager import fm
from Maix import GPIO
import KPU as kpu

from Maix import GPIO, I2S, FFT
import image, lcd, math
from board import board_info
from fpioa_manager import fm

from es8374 import ES8374
from Maix import I2S
from fpioa_manager import *
import audio
import time

# from machine import Timer

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

i2c = I2C(I2C.I2C3, freq=600*1000, sda=27, scl=24)  # amigo
print(i2c.scan())

axp173 = AXP173(i2c)
axp173.writeREG(0x27, 0x20)
axp173.writeREG(0x28, 0x0C)

#lcd.init(type=1)

#clock = time.clock()
##sensor.reset(choice=1, dual_buff=True)
#sensor.reset(choice=1)
#sensor.set_pixformat(sensor.YUV422)
#sensor.set_framesize(sensor.QVGA)
#sensor.set_hmirror(1)
#sensor.set_vflip(1)
#sensor.skip_frames(time=2000)
##sensor.set_windowing((448, 448))
#sensor.run(1)

#task = kpu.load(0x2C0000) # you need put model(face.kfpkg) in flash at address 0x300000
##task = kpu.load("/sd/0x2C0000_facedetect.kmodel")
#anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
#a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

#while True:
  #k = sensor.snapshot()
  #k.pix_to_ai()
  #code = kpu.run_yolo2(task, k)
  #if code:
      #for pos in range(len(code)):
          #i = code[pos]
          #k.draw_rectangle(i.x(), i.y(), i.w(), i.h(), thickness=5, color=(255,0,0))

  #lcd.display(k)
  #continue

class CubeAudio:

    i2c, i2s, dev = None, None, None

    # tim = Timer(Timer.TIMER0, Timer.CHANNEL0, start=False, mode=Timer.MODE_PERIODIC, period=15, callback=lambda:None)

    def init(i2c_dev=None):
        CubeAudio.i2c = i2c_dev

    def check():
      if CubeAudio.i2c != None:
        return ES8374._ES8374_I2CADDR_DEFAULT in CubeAudio.i2c.scan()
      return False

    player, is_load, is_ready = None, False, False

    def ready(is_record=False, volume=100):
      CubeAudio.is_ready = CubeAudio.is_load = False
      if CubeAudio.check():
        if CubeAudio.dev != None:
            CubeAudio.dev.stop(0x02)
        CubeAudio.dev = ES8374(CubeAudio.i2c)
        CubeAudio.dev.setVoiceVolume(volume)
        CubeAudio.dev.start(0x03)
        CubeAudio.i2s = I2S(I2S.DEVICE_0, pll2=262144000, mclk=31)
        if is_record:
            CubeAudio.i2s.channel_config(I2S.CHANNEL_0, I2S.RECEIVER, resolution=I2S.RESOLUTION_16_BIT,
                                         cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)
        else:
            CubeAudio.i2s.channel_config(I2S.CHANNEL_2, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                                         cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)
        CubeAudio.is_ready = True
      return CubeAudio.is_ready

    def load(path, volume=100):
        if CubeAudio.player != None:
            CubeAudio.player.finish()
            # CubeAudio.tim.stop()
        CubeAudio.player = audio.Audio(path=path)
        CubeAudio.player.volume(volume)
        wav_info = CubeAudio.player.play_process(CubeAudio.i2s)
        CubeAudio.i2s.set_sample_rate(int(wav_info[1]))

        CubeAudio.is_load = True
        # CubeAudio.tim.callback(CubeAudio.event)
        # CubeAudio.tim.start()
        #time.sleep_ms(1000)

    def event(arg=None):
        if CubeAudio.is_load:
            ret = CubeAudio.player.play()
            if ret == None or ret == 0:
                CubeAudio.player.finish()
                time.sleep_ms(50)
                # CubeAudio.tim.stop()
                CubeAudio.is_load = False
            return True
        return False


if __name__ == "__main__":
    from machine import I2C
    # fm.register(24, fm.fpioa.I2C1_SCLK, force=True)
    # fm.register(27, fm.fpioa.I2C1_SDA, force=True)
    #fm.register(30,fm.fpioa.I2C1_SCLK, force=True)
    #fm.register(31,fm.fpioa.I2C1_SDA, force=True)

    #i2c = I2C(I2C.I2C3, freq=600*1000, sda=27, scl=24)  # amigo
    #i2c = I2C(I2C.I2C3, freq=100*1000, scl=30, sda=31)  # cube
    print(i2c.scan())
    CubeAudio.init(i2c)
    tmp = CubeAudio.check()
    print(tmp)
    if (tmp):
        # cube
        #fm.register(19,fm.fpioa.I2S0_MCLK, force=True)
        #fm.register(35,fm.fpioa.I2S0_SCLK, force=True)
        #fm.register(33,fm.fpioa.I2S0_WS, force=True)
        #fm.register(34,fm.fpioa.I2S0_IN_D0, force=True)
        #fm.register(18,fm.fpioa.I2S0_OUT_D2, force=True)

        # amigo
        fm.register(13, fm.fpioa.I2S0_MCLK, force=True)
        fm.register(21, fm.fpioa.I2S0_SCLK, force=True)
        fm.register(18, fm.fpioa.I2S0_WS, force=True)
        fm.register(35, fm.fpioa.I2S0_IN_D0, force=True)
        fm.register(34, fm.fpioa.I2S0_OUT_D2, force=True)

        #CubeAudio.ready()
        #while True:
            #CubeAudio.load(path="/sd/res/sound/loop.wav")
            #while CubeAudio.is_load:
                ##time.sleep_ms(20)
                #CubeAudio.event()
                #print(time.ticks_ms())
        sample_rate = 38640
        sample_points = 1024
        fft_points = 512
        hist_x_num = 50

        img = image.Image(size=(240, 240))
        if hist_x_num > 320:
            hist_x_num = 320
        hist_width = int(320 / hist_x_num)#changeable
        x_shift = 0

        while True:
          # record to wav
          print('record to wav')
          CubeAudio.ready(True)
          CubeAudio.i2s.set_sample_rate(sample_rate)

          # init audio
          player = audio.Audio(path="/sd/record_4.wav",
                               is_create=True, samplerate=sample_rate)
          queue = []
          lcd.init()
          for i in range(500):
            tmp = CubeAudio.i2s.record(sample_points)
            if len(queue) > 0:
                print(time.ticks())
                ret = player.record(queue[0])
                #fft_res = FFT.run(tmp.to_bytes(), fft_points)
                #fft_amp = FFT.amplitude(fft_res)
                #img = img.clear()
                #x_shift = 0
                #for i in range(hist_x_num):
                    #if fft_amp[i] > 240:
                        #hist_height = 240
                    #else:
                        #hist_height = fft_amp[i]
                    #img = img.draw_rectangle((x_shift,240-hist_height,hist_width,hist_height),[255,255,255],2,True)
                    #x_shift = x_shift + hist_width
                #lcd.display(img)
                #fft_amp.clear()
                queue.pop(0)

            #k = sensor.snapshot()
            #k.pix_to_ai()
            #code = kpu.run_yolo2(task, k)
            #if code:
                #for pos in range(len(code)):
                    #i = code[pos]
                    #k.draw_rectangle(i.x(), i.y(), i.w(), i.h(), thickness=5, color=(255,0,0))

            #lcd.display(k)
            #continue

            CubeAudio.i2s.wait_record()
            queue.append(tmp)

            #fft_res = FFT.run(tmp.to_bytes(), fft_points)
            #fft_amp = FFT.amplitude(fft_res)
            #img = img.clear()
            #x_shift = 0
            #for i in range(hist_x_num):
                #if fft_amp[i] > 240:
                    #hist_height = 240
                #else:
                    #hist_height = fft_amp[i]
                #img = img.draw_rectangle((x_shift,240-hist_height,hist_width,hist_height),[255,255,255],2,True)
                #x_shift = x_shift + hist_width
            #fft_amp.clear()
            #lcd.display(img)
            #lcd.clear((255,0,0))

          player.finish()

          print('play to wav')
          CubeAudio.ready()
          CubeAudio.load("/sd/record_4.wav")
          while CubeAudio.is_load:
              #time.sleep_ms(20)
              CubeAudio.event()
              print(time.ticks_ms())
              #k = sensor.snapshot()
              ##img.pix_to_ai()
              #code = kpu.run_yolo2(task, k)
              #if code:
                  #for pos in range(len(code)):
                      #i = code[pos]
                      #k.draw_rectangle(i.x(), i.y(), i.w(), i.h(), thickness=5, color=(255,255,255))
              #lcd.display(k)

