# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math

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
from button import sipeed_button, button_io
from wdt import protect
from led import cube_led
from sound import CubeAudio
#from ui_taskbar import taskbar

class app:

    layer = 0 # set help_draw to top
    ctrl = agent()
    btn = sipeed_button()
    loop = 0
    loading = False

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
    #@ui.warp_template(taskbar.battery_draw)
    # @ui.warp_template(taskbar.mem_draw)
    @ui.warp_template(ui.bg_in_draw)
    def draw_launcher():
        ui.display()

    #@ui.warp_template(CubeAudio.event)
    @ui.warp_template(ui.anime_draw)
    #@ui.warp_template(CubeAudio.event)
    #@ui.warp_template(taskbar.mem_draw)
    # @ui.warp_template(system_info.info_draw)
    def draw_pages():
        if app.current != None:
            app.current.draw()
        ui.display()

    #@ui.warp_template(taskbar.time_draw)
    #@ui.warp_template(sample_page.sample_draw)
    #@ui.warp_template(ui.grey_draw)
    #@ui.warp_template(CubeAudio.event)
    def draw_samples():
        ui.display()

    @ui.warp_template(CubeAudio.event)
    #@ui.warp_template(explorer.draw)
    def draw_explorer():
        # if explorer.info != "":
        #     protect.stop()
        #     print(explorer.get_path(explorer.paths) + '/' + explorer.info)
        #     # with open(explorer.get_path(explorer.paths) + '/' + tmp, 'rb') as target:
        #     #     # exec(target.read(), locals())
        #     #     exec(target.read())
        #     execfile(explorer.get_path(explorer.paths) + '/' + explorer.info)
        #     protect.start()

        app.loop = (app.loop + 1) % 250
        value = math.cos(math.pi * app.loop / 16) * 10
        ui.canvas.draw_string(320, 280, "Music Playing...",
                              color=(164 + int(value) * 8, 164 + int(value) * 8, 164 + int(value) * 8), scale=2, mono_space=0)
        ui.display()

    def draw_camera():
        try:
            ai_camera.ai_draw()
            if ai_camera.models[1].bbox != None:
                bbox = ai_camera.models[1].bbox
                for i in bbox:
                    # print(i)
                    ui.canvas.draw_string(100, 280, "Music Playing...")
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
        elif selected == 2:
            CubeAudio.load(os.getcwd() + "/res/loop.wav", 100)
            pass
            #app.layer -= 1 # return last layer
            #raise Exception("Settings Unrealized.")
        elif selected == 3:
            #sample_page.key_init()
            #sample_page.add_sample(sample_msa301())
            #sample_page.add_sample(sample_spmod_test())
            #sample_page.add_sample(sample_shtxx())
            #sample_page.add_demo()
            pass


    def exec_application():
        if launcher.app_select == 0:
            app.draw_camera()
        if launcher.app_select == 1:
            app.draw_pages()
        if launcher.app_select == 2:
            app.draw_explorer()
        if launcher.app_select == 3:
            try:
                app.draw_samples()
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

        fm.register(24,fm.fpioa.I2C1_SCLK, force=True)
        fm.register(27,fm.fpioa.I2C1_SDA, force=True)
        i2c = I2C(I2C.I2C1, freq=100*1000)
        print('monkey patch for i2c')
        from fpioa_manager import fm
        from Maix import GPIO
        tmp = fm.fpioa.get_Pin_num(fm.fpioa.I2C1_SDA)
        fm.register(tmp, fm.fpioa.GPIOHS15)
        sda = GPIO(GPIO.GPIOHS15, GPIO.OUT)
        sda.value(1)
        fm.register(tmp, fm.fpioa.I2C1_SDA, force=True)
        if AXP173_ADDR in i2c.scan():
            axp173 = AXP173(i2c_dev=i2c)
            if (48 != axp173.getPowerWorkMode()):
                axp173.enable_adc(True)
                # 默认充电限制在 4.2V, 190mA 档位
                axp173.setEnterChargingControl(True)
                axp173.exten_output_enable()
                # amigo sensor config.
                axp173.writeREG(0x27, 0x20)
                axp173.writeREG(0x28, 0x0C)

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
            last = time.ticks_ms()
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
