# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc

try:
    from core import agent
    from ui_canvas import ui, print_mem_free
    # from ui_launcher import launcher
    from ui_3d_launcher import launcher
    from ui_system_info import system_info
    from ui_catch import catch
    from ui_pages import pages
    from ui_camera import ai_camera
    from ui_sample import sample_page
    from ui_explorer import explorer
    from sample_shtxx import sample_shtxx
    from sample_spmod import sample_spmod_test
    from sample_msa301 import sample_msa301
    from button import cube_button
    from wdt import protect
    from led import cube_led
    from sound import CubeAudio
    from ui_taskbar import taskbar
except ImportError:
    from lib.core import agent
    from ui.ui_canvas import ui, print_mem_free
    # from ui.ui_launcher import launcher
    from ui.ui_3d_launcher import launcher
    from ui.ui_system_info import system_info
    from ui.ui_catch import catch
    from ui.ui_pages import pages
    from ui.ui_camera import ai_camera
    from ui.ui_sample import sample_page
    from ui.ui_explorer import explorer
    from ui.sample_shtxx import sample_shtxx
    from ui.sample_spmod import sample_spmod_test
    from ui.sample_msa301 import sample_msa301
    from driver.button import cube_button
    from driver.wdt import protect
    from driver.led import cube_led
    from ui.ui_taskbar import taskbar
    from driver.sound import CubeAudio

class app:

    layer = 0 # set help_draw to top
    ctrl = agent()
    btn = cube_button()

    @ui.warp_template(ui.bg_in_draw)
    @ui.warp_template(ui.help_in_draw)
    def draw_load():
        ui.display()

    # @ui.warp_template(ui.bg_in_draw) # ui_3d_launcher need remove
    @ui.warp_template(launcher.draw)
    #@ui.warp_template(taskbar.mem_draw)
    @ui.warp_template(taskbar.battery_draw)
    # @ui.warp_template(taskbar.mem_draw)
    def draw_launcher():
        ui.display()

    @ui.warp_template(CubeAudio.event)
    @ui.warp_template(ui.anime_draw)
    @ui.warp_template(CubeAudio.event)
    @ui.warp_template(taskbar.mem_draw)
    # @ui.warp_template(system_info.info_draw)
    def draw_pages():
        if app.current != None:
            app.current.draw()
        ui.display()

    @ui.warp_template(CubeAudio.event)
    @ui.warp_template(taskbar.time_draw)
    @ui.warp_template(sample_page.sample_draw)
    @ui.warp_template(CubeAudio.event)
    def draw_samples():
        ui.display()

    @ui.warp_template(explorer.draw)
    def draw_explorer():
        # if explorer.info != "":
        #     protect.stop()
        #     print(explorer.get_path(explorer.paths) + '/' + explorer.info)
        #     # with open(explorer.get_path(explorer.paths) + '/' + tmp, 'rb') as target:
        #     #     # exec(target.read(), locals())
        #     #     exec(target.read())
        #     execfile(explorer.get_path(explorer.paths) + '/' + explorer.info)
        #     protect.start()

        ui.display()

    def draw_camera():
        try:
            ai_camera.ai_draw()
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
            CubeAudio.load(os.getcwd() + "/res/alarm.wav", 100)
            app.current = pages()
        elif selected == 2:
            pass
            #app.layer -= 1 # return last layer
            #raise Exception("Settings Unrealized.")
        elif selected == 3:
            CubeAudio.load(os.getcwd() + "/res/one.wav", 100)
            sample_page.add_sample(sample_msa301())
            sample_page.add_sample(sample_spmod_test())
            sample_page.add_sample(sample_shtxx())
            sample_page.add_demo()


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
    @ui.warp_template(ui.grey_draw)
    @catch
    def draw():

        #app.btn.event()
        app.btn.expand_event()

        if app.btn.home() == 2: # click button release to 2
            print('into', app.layer)
            if app.layer == 1:
                app.layer += 1
                # launcher into application
                app.load_application(launcher.app_select)
            elif app.layer == 2:
                if app.btn.interval() > 1000: # long press
                    app.layer -= 1
                # application return launcher
            else:
                app.layer += 1
                # help into launcher

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
        CubeAudio.ready()
        #app.ctrl.event(100, lambda *args: time.sleep(1))
        #app.ctrl.event(10, app.btn.event)
        app.ctrl.event(5, app.draw)
        while True:
            #import time
            #last = time.ticks_ms()
            while True:
                try:
                    #print((int)(1000 / (time.ticks_ms() - last)), 'fps')
                    #last = time.ticks_ms()
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
