# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

# !!! sipeed cube special !!!
# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
from core import agent
from ui_canvas import ui, print_mem_free
from ui_taskbar import taskbar
from ui_launcher import launcher
from ui_system_info import system_info
from ui_catch import catch
from ui_pages import pages
from button import cube_button
from ui_camera import ai_camera


class app:

    layer = 0  # set help_draw to top
    ctrl = agent()
    btn = cube_button()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(ui.help_draw)
    def draw_load():
        ui.display()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(taskbar.mem_draw)
    @ui.warp_template(launcher.draw)
    def draw_launcher():
        ui.display()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(ui.anime_draw)
    @ui.warp_template(taskbar.mem_draw)
    # @ui.warp_template(system_info.info_draw)
    def draw_pages():
        if app.current != None:
            app.current.draw()
        ui.display()

    applist = ['Camera', 'Settings', 'Explorer', 'Statistics']
    current = None

    def draw_camera():
        try:
            ai_camera.ai_draw()
            ui.display()
        except Exception as e:
            app.layer = 1
            raise e

    def load_application(selected):
        # system_info.info = ''
        if app.current != None:  # clear last application
            del app.current
            app.current = None
        if selected == 0:
            # system_info.info = '  selected:\n    %s' % (app.applist[selected])
            pass
        elif selected == 1:
            app.current = pages()
        elif selected == 2:
            app.layer -= 1  # return last layer
            raise Exception("Settings Unrealized.")
        elif selected == 3:
            # system_info.info = '  selected:\n    %s' % (app.applist[selected])
            pass

    def exec_application():
        if launcher.app_select == 0:
            app.draw_camera()
        if launcher.app_select == 1:
            app.draw_pages()
        if launcher.app_select == 2:
            pass
        if launcher.app_select == 3:
            app.draw_pages()

    @ui.warp_template(ui.blank_draw)
    @catch
    def draw():

        app.btn.event()

        if app.btn.home() == 2:  # click button release to 2
            if app.layer == 1:
                app.layer += 1
                # launcher into application
                app.load_application(launcher.app_select)
            elif app.layer == 2:
                app.layer -= 1
                # application return launcher
            else:
                app.layer += 1
                # help into launcher

        if app.layer == 0:
            app.draw_load()
        elif app.layer == 1:
            app.draw_launcher()
        elif app.layer == 2:
            app.exec_application()

    def run():
        #app.ctrl.event(100, lambda *args: time.sleep(1))
        #app.ctrl.event(10, app.btn.event)
        app.ctrl.event(10, app.draw)
        while True:
            import time
            last = time.ticks_ms()
            while True:
                try:
                    print((int)(1000 / (time.ticks_ms() - last)), 'fps')
                    last = time.ticks_ms()
                    app.ctrl.parallel_cycle()
                    #time.sleep(0.1)
                except Exception as e:
                    gc.collect()
                    print(e)


if __name__ == "__main__":
    print_mem_free()
    app.run()
