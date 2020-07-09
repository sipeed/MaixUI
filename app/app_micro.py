# This file is part of MaixUI
# Copyright (c) 2020 sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
from core import agent
from ui_maix import ui, print_mem_free
from ui_taskbar import taskbar
from ui_launcher import launcher
from ui_system_info import system_info
from ui_catch import catch
from ui_user import user
from button import cube_button
from ui_camera import test_camera

class app:

    index = 0
    ctrl = agent()
    btn = cube_button()

    @ui.warp_template(ui.bg_in_draw)
    @ui.warp_template(ui.help_in_draw)
    def load():
        ui.display()

    @ui.warp_template(ui.bg_in_draw)
    @ui.warp_template(taskbar.mem_draw)
    @ui.warp_template(launcher.draw)
    def main():
        ui.display()

    @ui.warp_template(ui.bg_in_draw)
    @ui.warp_template(ui.anime_in_draw)
    @ui.warp_template(taskbar.mem_draw)
    @ui.warp_template(system_info.info_draw)
    def user():
        if app.current:
            if launcher.app_select == 0:
                test_camera.info_draw()
                print(test_camera.info_draw)
            if launcher.app_select == 1:
                app.current.draw()
            if launcher.app_select == 3:
                app.current.draw()

        ui.display()

    pages = ['Camera', 'Settings', 'Explorer', 'Statistics']
    current = None

    @ui.warp_template(ui.bg_in_draw)
    @catch
    def draw():
        if app.index != 0:
            if app.btn.home() == 2:
                app.index = 2 if app.index == 1 else 1
                if app.current != None:
                    del app.current
                    app.current = None
                system_info.info = ""
                if launcher.app_select == 0:
                    system_info.info = '  selected:\n    %s' % (app.pages[launcher.app_select])
                    app.current = user()
                if launcher.app_select == 1:
                    app.current = user()
                if launcher.app_select == 2:
                    app.index = 1
                    raise Exception("Settings Unrealized.")
                if launcher.app_select == 3:
                    system_info.info = '  selected:\n    %s' % (app.pages[launcher.app_select])

        elif app.btn.home() == 2:
            app.index = 1

        if app.index == 0:
            app.load()
        elif app.index == 1:
            app.main()
        elif app.index == 2:
            app.user()

        app.btn.event()

    def run():
        #app.ctrl.event(100, lambda *args: time.sleep(1))
        #app.ctrl.event(10, app.btn.event)
        app.ctrl.event(10, app.draw)
        while True:
            import time
            last = time.ticks_ms()
            while True:
                try:
                    print(time.ticks_ms() - last)
                    last = time.ticks_ms()
                    app.ctrl.cycle()
                    #time.sleep(0.1)
                except Exception as e:
                    gc.collect()
                    print(e)


if __name__ == "__main__":
    print_mem_free()
    app.run()
