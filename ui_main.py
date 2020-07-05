
import time
from core import agent
from maix_ui import ui
from ui_taskbar import taskbar
from ui_system_info import system_info
from button import cube_button

class app:

    index = 0
    ctrl = agent()
    cube_btn = cube_button()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(system_info.info_draw1)
    def draw0():
        ui.display()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(taskbar.time_draw)
    @ui.warp_template(system_info.info_draw2)
    def draw1():
        ui.display()

    @ui.warp_template(ui.logo_draw)
    @ui.warp_template(taskbar.time_draw)
    def draw2():
        ui.display()

    def draw():

        if app.cube_btn.back() == 2:
            app.index = 1
        elif app.cube_btn.next() == 2:
            app.index = 2
        elif app.cube_btn.home() == 2:
            app.index = 0

        if app.index == 1:
            app.draw1()
        elif app.index == 2:
            app.draw2()
        else:
            app.draw0()

    def run():
        #app.ctrl.event(100, lambda *args: time.sleep(1))
        app.ctrl.event(10, app.draw)
        app.ctrl.event(10, app.cube_btn.event)
        while True:
            app.ctrl.cycle()
            #time.sleep(0.1)

if __name__ == "__main__":
    app.run()
