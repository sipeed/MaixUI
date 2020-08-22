# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math, ulab

from core import agent
from ui_canvas import ui, print_mem_free
# from ui_launcher import launcher
from ui_amigo_launcher import launcher
from ui_system_info import system_info
from ui_catch import catch
from ui_pages import pages
from ui_camera import ai_camera
from ui_sample import sample_page
from ui_explorer import explorer
#from sample_shtxx import sample_shtxx
#from sample_spmod import sample_spmod_test
#from sample_msa301 import sample_msa301
from msa301 import MSA301, _MSA301_I2CADDR_DEFAULT
from button import sipeed_button, button_io
from wdt import protect
from led import cube_led
from sound import CubeAudio
from touch import Touch, TouchLow
from ui_taskbar import taskbar
from shtxx import SHT3x, SHT3x_ADDR, SHT31_ADDR

class app:

    layer = 0 # set help_draw to top
    ctrl = agent()
    btn = sipeed_button()
    loop = 0
    loading = False
    toth = Touch(480, 320, 50)
    touch_select = 0
    msa301 = None

    def touch_draw():
        app.toth.event()

        app.loop = (app.loop + 1) % 200

        value = math.cos(math.pi * app.loop / 32) * 8

        # temp code
        tmp_x, tmp_l, tmp_r = 0, 0, 0

        if app.toth.state == 2:
          #print(app.toth.state, app.toth.points)
          p = app.toth.points[1]
          if p[0] > 430 and p[1] > 260:
            app.layer -= 1
          elif p[0] < 60 and p[1] < 60:
            app.touch_select = -1
            #print(app.touch_select)
            if launcher.app_select == 1:
                app.current.page -= 1
            elif launcher.app_select == 3:
                pass
          elif p[0] > 420 and p[1] < 60:
            app.touch_select = +1
            #print(app.touch_select)
            if launcher.app_select == 1:
                app.current.page -= 1
            elif launcher.app_select == 3:
                pass

        if app.toth.state == 1:
            p = app.toth.points[1]
            if p[0] > 430 and p[1] > 270:
                tmp_x = int(value) + 30
            elif p[0] < 50 and p[1] < 50:
                tmp_l = int(value) + 30
            elif p[0] > 430 and p[1] < 50:
                tmp_r = int(value) + 30

        ui.canvas.draw_circle(ui.height, 0, 42 + tmp_x, thickness=8, fill=False, color=(100, 100, 100))
        ui.canvas.draw_circle(ui.height, 0, 38 + tmp_x, fill=True, color=(255, 255, 255))
        ui.canvas.draw_string(ui.height - 15, 5, "x", scale=2, color=(0, 0, 0))

        ui.canvas.draw_circle(0, ui.weight, 42 + tmp_l, thickness=8, fill=False, color=(100, 100, 100))
        ui.canvas.draw_circle(0, ui.weight, 38 + tmp_l, fill=True, color=(255, 255, 100))
        ui.canvas.draw_string(10, ui.weight - 30, "<", scale=2, color=(0, 0, 0))

        ui.canvas.draw_circle(ui.height, ui.weight, 42 + tmp_r, thickness=8, fill=False, color=(100, 100, 100))
        ui.canvas.draw_circle(ui.height, ui.weight, 38 + tmp_r, fill=True, color=(100, 255, 255))
        ui.canvas.draw_string(ui.height - 15, ui.weight - 30, ">", scale=2, color=(0, 0, 0))

    #@ui.warp_template(CubeAudio.event)
    @ui.warp_template(ui.bg_in_draw)
    #@ui.warp_template(ui.help_in_draw)
    def draw_load():

        app.loop = (app.loop + 1) % 200

        value = math.cos(math.pi * app.loop / 8) * 6

        #print(value)
        if app.loading or app.loop > 20:

            ui.canvas.draw_string(200 - int(value) * 2, 68 + (int(value) % 8) * 2, "A",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200 - int(value), 72 + (int(value) % 8), "A",
                                color=(0xFF, 0x40, 0x40), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 73, "A", color=(64, 64, 64), scale=8, mono_space=0)

        if app.loading or app.loop > 40:

            ui.canvas.draw_string(203, 72 - int(value) * 5 - 9, "  m",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200, 70 - int(value) * 4 - 8, "  m",
                                color=(0xFF, 0xFF, 0x40), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "  m",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if app.loading or app.loop > 40:

            ui.canvas.draw_string(203, 72, "    i",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200, 70, "    i",
                                color=(0x40, 0x40, 0xFF), scale=8, mono_space=0)

            ui.canvas.draw_rectangle((304, 77, 12, 12),
                                color=(0, 0, 0), fill=True)

            ui.canvas.draw_string(259, 44 + int(value), "    .    ",
                                color=(64, 64, 64), scale=4, mono_space=0)
            ui.canvas.draw_string(256, 42 + int(value), "    .    ",
                                color=(0x40, 0x40, 0xFF), scale=4, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "    i",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_rectangle((304, 77, 12, 12),
                                color=(0, 0, 0), fill=True)
            ui.canvas.draw_string(259, 44, "    .    ",
                                color=(64, 64, 64), scale=4, mono_space=0)

        if app.loading or app.loop > 60:

            ui.canvas.draw_string(203 + int(value) * 2 + 10, 72, "     g",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200 + int(value) * 2 + 10, 70, "     g",
                                color=(0x40 + int(value) * 50, 0xFF, 0x40 + int(value) * 50), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "     g",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if app.loading or app.loop > 60:

            ui.canvas.draw_string(203 - int(value) * 2 + 20, 72, "       o",
                                color=(64, 64, 64), scale=8, mono_space=0)
            ui.canvas.draw_string(200 - int(value) * 2 + 20, 70, "       o",
                                color=(0xFF, 0x50 + int(value) * 50, 0xFF), scale=8, mono_space=0)
        else:
            ui.canvas.draw_string(203, 72, "       o",
                                color=(64, 64, 64), scale=8, mono_space=0)

        if app.loading == False and app.loop < 20:

            ui.canvas.draw_string(203, 73, "Amigo",
                                  color=(64 + int(value) * 2, 64 + int(value) * 2, 64 + int(value) * 2), scale=8, mono_space=0)

        if app.loop > 70:
            app.loading = True;
            ui.canvas.draw_string(320, 280, "Now Loading...",
                                  color=(164 + int(value) * 8, 164 + int(value) * 8, 164 + int(value) * 8), scale=2, mono_space=0)

        if app.loop == 100:
            app.layer += 1

        ui.display()

    # @ui.warp_template(ui.bg_in_draw) # ui_3d_launcher need remove
    @ui.warp_template(launcher.draw)
    #@ui.warp_template(taskbar.mem_draw)
    @ui.warp_template(taskbar.battery_draw)
    @ui.warp_template(ui.bg_in_draw)
    def draw_launcher():
        ui.display()

    #@ui.warp_template(CubeAudio.event)
    @ui.warp_template(ui.grey_draw)
    @ui.warp_template(ui.anime_draw)
    @ui.warp_template(touch_draw)
    #@ui.warp_template(CubeAudio.event)
    #@ui.warp_template(taskbar.mem_draw)
    # @ui.warp_template(system_info.info_draw)
    def draw_pages():
        if app.current != None:
            app.current.draw()

        app.loop = (app.loop + 1) % 200

        value = math.cos(math.pi * app.loop / 12) * 2 + 20

        ui.canvas.draw_rectangle((240, 0, 240, 320), fill=False, thickness=3, color=(175, 175, 175))
        acceleration = app.msa301.acceleration
        x, y = 360, 160 # center
        #print(acceleration)
        ui.canvas.draw_circle(x + int(acceleration[0] * 15), y + int(acceleration[1] * 20), int(value), fill=True,
            color=(150 + int(acceleration[0] * 20), 150 + int(acceleration[1] * 20), 100 + int(acceleration[2] * 20)))  # 10ms
        ui.canvas.draw_circle(x + int(acceleration[0] * 15), y + int(acceleration[1] * 20), int(value) + 1, thickness=3, fill=False, color=(0, 0, 0))  # 10ms

        #ui.canvas.draw_string(240 + 10, 140, "x", (255, 0, 0), scale=2)
        #ui.canvas.draw_string(240 + 10, 140, "x", (255, 0, 0), scale=2)
        #ui.canvas.draw_line(240 + 120, 150, 120 + int(acceleration[0] * 8), 150, color=(41, 131, 255))
        #ui.canvas.draw_string(240 + 10, 160, "y", (0, 255, 0), scale=2)
        #ui.canvas.draw_line(240 + 120, 170, 120 + int(acceleration[1] * 8), 170, color=(141, 31, 255))
        #ui.canvas.draw_string(240 + 10, 180, "z", (0, 0, 255), scale=2)
        #ui.canvas.draw_line(240 + 120, 190, 120 + int(acceleration[2] * 8), 190, color=(241, 131, 55))

        ui.display()

    #@ui.warp_template(taskbar.time_draw)
    #@ui.warp_template(sample_page.sample_draw)
    #@ui.warp_template(ui.grey_draw)
    #@ui.warp_template(CubeAudio.event)
    @ui.warp_template(touch_draw)
    def draw_photos():
        ui.display()

    i2c0 = None
    sht3x = None
    sidu = None
    temp = 0
    points = []
    isconnected = False
    @ui.warp_template(touch_draw)
    #@ui.warp_template(taskbar.mem_draw)
    #@ui.warp_template(taskbar.time_draw)
    @ui.warp_template(CubeAudio.event)
    #@ui.warp_template(explorer.draw)
    def draw_demo():
        app.loop = (app.loop + 1) % 200
        value = math.cos(math.pi * app.loop / 16) * 10

        ui.canvas.draw_string(10, 5, "Seeed Grove",
                          color=(40 + int(value) * 2, 240 + int(value) * 2, 40 + int(value) * 2), scale=3, mono_space=0)

        try:
            if app.isconnected == False:
                CubeAudio.event()
                if app.loop % 10 == 0:
                    # print(app.loop)
                    # print(self.i2c.scan())
                    fm.register(9, fm.fpioa.I2C0_SCLK, force=True)
                    fm.register(7, fm.fpioa.I2C0_SDA, force=True)
                    if SHT3x_ADDR in app.i2c0.scan():
                        app.sht3x = SHT3x(app.i2c0, SHT3x_ADDR)
                        app.isconnected = True
                    if SHT31_ADDR in app.i2c0.scan():
                        app.sht3x = SHT3x(app.i2c0, SHT31_ADDR)
                        app.isconnected = True

                ui.canvas.draw_string(280, 25, "Wait Grove Sensor \n sht31/35 <<<  <<  <-",
                                      color=(140 + int(value) * 5, 240 + int(value) * 5, 140 + int(value) * 5), scale=2, mono_space=0)

                if CubeAudio.event() == False:

                    value = math.cos(math.pi * app.loop / 100) * 50

                    tmp = int(value)
                    #print(value)

                    ui.canvas.draw_circle(0, 0, 100 + tmp, fill=False, color=(0, (150 + tmp) + 10, 0))
                    ui.canvas.draw_circle(0, 0, 100 + tmp * 2, fill=False, color=(0, (150 + tmp) + 20, 0))
                    ui.canvas.draw_circle(0, 0, 100 + tmp * 3, fill=False, color=(0, (150 + tmp) + 30, 0))
                    ui.canvas.draw_circle(0, 0, 100 + tmp * 4, fill=False, color=(0, (150 + tmp) + 40, 0))

            else:
                CubeAudio.event()
                data = app.sht3x.read_temp_humd()
                if app.sidu == None:
                    app.sidu = image.Image(os.getcwd() + "/res/sidu.jpg")

                ui.canvas.draw_circle(350, 160, 100, fill=True, color=(255, 255, 255))
                ui.canvas.draw_image(app.sidu, 270, 60, alpha=235 + int(value) * 2)
                ui.canvas.draw_string(330, 190, "%.2d" % data[1], scale=4, color=(80, 80, 80))

                ui.canvas.draw_rectangle(60, 60, 180, 200, thickness=4, color=(155, 155, 155))
                if len(app.points) > 18:
                    app.points.pop(0)
                elif app.temp != int(data[0] * 10):
                    app.temp = int(data[0] * 10)
                    app.points.append(app.temp)
                for p in range(len(app.points)):
                    #print(app.points)
                    if p < 1:
                        b = (60 + int(10 * (p))), 450 - app.points[p]
                        ui.canvas.draw_circle(b[0], b[1], 3, fill=True, color=(255, 155, 150))
                    else:
                        a, b = ((60 + int(10 * (p-1))), 450 - app.points[p-1]), ((60 + int(10 * (p))), 450 - app.points[p])
                        ui.canvas.draw_circle(b[0], b[1], 3, fill=False, color=(155, 155, 155))
                        ui.canvas.draw_line(a[0], a[1], b[0], b[1], thickness=4, color=(255,255,255))

                ui.canvas.draw_string(60, 280, "Average temperature: %s" % str(ulab.mean(app.points) / 10.0),
                                      color=(240 + int(value) * 5, 240 + int(value) * 5, 240 + int(value) * 5), scale=2, mono_space=0)

                CubeAudio.event()
            ui.display()
        except Exception as e:
            app.layer = 1
            app.isconnected = False
            raise e

    def draw_camera():
        try:
            ai_camera.ai_draw()
            if ai_camera.models[1].bbox != None:
                bbox = ai_camera.models[1].bbox
                ui.canvas.draw_string(20, 260, "Find Face %d" % len(bbox), scale=5)
                for pos in range(len(bbox)):
                    i = bbox[pos]
                    print(i.x(), i.y(), i.w(), i.h())
                    face_cut = ui.canvas.cut(i.x(), i.y(), i.w(), i.h())
                    face_cut_128 = face_cut.resize(80, 80)
                    ui.canvas.draw_image(face_cut_128, 320 + int((pos % 2)*80), int((pos // 2)*80))
            app.touch_draw()
            ui.display()
        except Exception as e:
            app.layer = 1
            raise e

    current = None

    def load_application(selected):
        if app.current != None: # clear last application
            del app.current
            app.current = None
        if selected == 0:
            pass

        elif selected == 1:
            app.current = pages()
            app.current.tips = "Weclome to Maix Amigo"
        elif selected == 2:
            CubeAudio.load(os.getcwd() + "/res/loop.wav", 100)
            pass
            #app.layer -= 1 # return last layer
            #raise Exception("Settings Unrealized.")
        elif selected == 3:
            pass


    def exec_application():
        if launcher.app_select == 0:
            app.draw_camera()
        if launcher.app_select == 1:
            app.draw_pages()
        if launcher.app_select == 2:
            app.draw_demo()
        if launcher.app_select == 3:
            try:
                app.draw_photos()
            except Exception as e:
                app.layer -= 1

    rgb = 0
    def rgb_change(rgb):
        cube_led.r.value(rgb & 0b001)
        cube_led.g.value(rgb & 0b010)
        cube_led.b.value(rgb & 0b100)

    @ui.warp_template(ui.blank_draw)
    #@ui.warp_template(ui.grey_draw)
    @catch
    def draw():

        #app.btn.event()
        app.btn.expand_event()
        if app.btn.home() == 2 or launcher.app_run: # click button release to 2
            launcher.app_run = False
            print('into', app.layer)
            if app.layer == 1:
                app.layer += 1
                # launcher into application
                app.load_application(launcher.app_select)
            elif app.layer == 2:
                if app.btn.interval() > 1000: # long press
                    app.layer -= 1
                    if launcher.app_select == 1:
                        ui.anime = None # Clear
                # application return launcher
            else:
                app.layer += 1
                # help into launcher
        #launcher.btn.enable = True

        #if launcher.app_run:
            #launcher.app_run = False
            #print('launcher.app_select', launcher.app_select)

        if app.btn.next() == 1:
            app.rgb = (app.rgb + 1) % 8
            app.rgb_change(app.rgb)

        if app.btn.back() == 1:
            app.rgb = (app.rgb - 1) % 8
            app.rgb_change(app.rgb)

        if app.layer == 0:
            app.draw_load()
        elif app.layer == 1:
            gc.collect()
            app.draw_launcher()
        elif app.layer == 2:
            app.exec_application()

    def run():
        ui.height, ui.weight = 480, 320
        button_io.config(23, 31, 20) # amigo
        cube_led.init(14, 15, 17, 32)

        # about sensor
        from pmu_axp173 import AXP173, AXP173_ADDR
        from machine import I2C
        from fpioa_manager import fm

        app.i2c0 = I2C(I2C.I2C0, freq=100*1000)

        fm.register(24,fm.fpioa.I2C1_SCLK, force=True)
        fm.register(27,fm.fpioa.I2C1_SDA, force=True)

        i2c = I2C(I2C.I2C1, freq=400*1000)
        print('monkey patch & config for i2c')
        from fpioa_manager import fm
        from Maix import GPIO
        tmp = fm.fpioa.get_Pin_num(fm.fpioa.I2C1_SDA)
        fm.register(tmp, fm.fpioa.GPIOHS15)
        sda = GPIO(GPIO.GPIOHS15, GPIO.OUT)
        sda.value(1)
        fm.register(tmp, fm.fpioa.I2C1_SDA, force=True)

        TouchLow.config(i2c) # amigo
        app.msa301 = MSA301(i2c)
        #if AXP173_ADDR in i2c.scan():
        axp173 = AXP173(i2c_dev=i2c)
        axp173.enable_adc(True)
        # 默认充电限制在 4.2V, 190mA 档位
        axp173.setEnterChargingControl(True)
        axp173.exten_output_enable()
        # amigo sensor config.
        axp173.writeREG(0x27, 0x20)
        axp173.writeREG(0x28, 0x0C)
        taskbar.init(axp173)

        if CubeAudio.check():
            CubeAudio.ready()
            fm.register(13,fm.fpioa.I2S0_MCLK, force=True)
            fm.register(21,fm.fpioa.I2S0_SCLK, force=True)
            fm.register(18,fm.fpioa.I2S0_WS, force=True)
            fm.register(35,fm.fpioa.I2S0_IN_D0, force=True)
            fm.register(34,fm.fpioa.I2S0_OUT_D2, force=True)

        #app.ctrl.event(100, lambda *args: time.sleep(1))
        #app.ctrl.event(10, app.btn.event)
        app.ctrl.event(5, app.draw)
        while True:
            import time
            last = time.ticks_ms() - 10.0
            while True:
                try:
                    print((int)(1000 / (time.ticks_ms() - last)), 'fps')
                    last = time.ticks_ms()
                    app.ctrl.cycle()
                    protect.keep()
                    #time.sleep(0.1)
                except KeyboardInterrupt:
                    protect.stop()
                    raise KeyboardInterrupt()
                except Exception as e:
                    gc.collect()
                    print(e)

if __name__ == "__main__":
    gc.collect()
    print_mem_free()
    app.run()
