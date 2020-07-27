
from es8374 import ES8374
from machine import I2C
from Maix import I2S, GPIO
from fpioa_manager import *
import audio, time
# from machine import Timer

class CubeAudio:

    i2c, i2s, dev = I2C(I2C.I2C0, freq=100*1000, sda=31,
                        scl=30), I2S(I2S.DEVICE_0, pll2=262144000, mclk=31), None

    # tim = Timer(Timer.TIMER0, Timer.CHANNEL0, start=False, mode=Timer.MODE_PERIODIC, period=15, callback=lambda:None)

    def check():
      return ES8374._ES8374_I2CADDR_DEFAULT in CubeAudio.i2c.scan()

    player, is_load, is_ready = None, False, False

    def ready(is_record=False):
      CubeAudio.is_ready = CubeAudio.is_load = False
      if CubeAudio.check():
        if CubeAudio.dev != None:
            CubeAudio.dev.stop(0x02)
        CubeAudio.dev = ES8374()
        fm.register(19, fm.fpioa.I2S0_MCLK, force=True)
        fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
        fm.register(33, fm.fpioa.I2S0_WS, force=True)
        fm.register(34, fm.fpioa.I2S0_IN_D0, force=True)
        fm.register(18, fm.fpioa.I2S0_OUT_D2, force=True)
        if is_record:
            CubeAudio.i2s.channel_config(I2S.CHANNEL_0, I2S.RECEIVER, resolution=I2S.RESOLUTION_16_BIT,
                cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)
        else:
            CubeAudio.i2s.channel_config(I2S.CHANNEL_2, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)

        CubeAudio.is_ready = True
      return CubeAudio.is_ready

    def set_record(sample_rate=22050):
      CubeAudio.i2s.set_sample_rate(sample_rate)

    def set_player(sample_rate=44100):
      CubeAudio.i2s.set_sample_rate(sample_rate)

    def load(path, volume=80):
        if CubeAudio.player != None:
            CubeAudio.player.finish()
            time.sleep_ms(10)
            # CubeAudio.tim.stop()
        CubeAudio.player = audio.Audio(path=path)
        CubeAudio.player.volume(volume)
        wav_info = CubeAudio.player.play_process(CubeAudio.i2s)
        CubeAudio.set_player(int(wav_info[1]))
        CubeAudio.is_load = True
        # CubeAudio.tim.callback(CubeAudio.event)
        # CubeAudio.tim.start()

    def event(arg=None):
        if CubeAudio.is_load:
            ret = CubeAudio.player.play()
            if ret == None or ret == 0:
                CubeAudio.player.finish()
                time.sleep_ms(10)
                # CubeAudio.tim.stop()
                CubeAudio.is_load = False

if __name__ == "__main__":

    if (CubeAudio.check()):

        CubeAudio.ready()
        while True:
            CubeAudio.load("/flash/183.wav", 50)
            while CubeAudio.is_load:
                time.sleep_ms(22)
                CubeAudio.event()
                print(time.ticks_ms())

        CubeAudio.ready()
        player = audio.Audio(path="/sd/record_5.wav")
        player.volume(100)
        # read audio info
        wav_info = player.play_process(CubeAudio.i2s)
        print("wav file head information: ", wav_info)
        CubeAudio.set_player(int(wav_info[1] / 2))
        print('loop to play audio')
        while True:
          ret = player.play()
          if ret == None:
              print("format error")
              break
          elif ret == 0:
              break
        player.finish()

        # record to wav
        print('record to wav')
        CubeAudio.ready()
        CubeAudio.set_record(22050)

        # init audio
        player = audio.Audio(path="/sd/record_5.wav",
                             is_create=True, samplerate=22050)
        queue = []
        for i in range(400):
          tmp = CubeAudio.i2s.record(1024)
          if len(queue) > 0:
              print(time.ticks())
              ret = player.record(queue[0])
              queue.pop(0)
          CubeAudio.i2s.wait_record()
          queue.append(tmp)
        player.finish()
