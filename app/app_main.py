
import time
from core import agent
from ui_maix import ui
from ui_taskbar import taskbar
from ui_launcher import launcher
from ui_system_info import system_info
from ui_user import user
from button import cube_button


class app:

    index = 0
    ctrl = agent()
    btn = cube_button()

    @ui.warp_template(ui.load_draw)
    @ui.warp_template(ui.logo_draw)
    def load():
        ui.display()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(taskbar.time_draw)
    @ui.warp_template(launcher.draw)
    def main():
        ui.display()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(ui.logo_draw)
    @ui.warp_template(taskbar.time_draw)
    @ui.warp_template(system_info.info_draw)
    def user():
        if app.current:
            if launcher.app_select == 1:
                app.current.draw()

            if launcher.app_select == 3:
                app.current.draw()
        ui.display()

    pages = ['Camera', 'Settings', 'Explorer', 'Statistics']
    current = None

    def draw():
        if app.index != 0:
            if app.btn.home() == 2:
                app.index = 2 if app.index == 1 else 1
                system_info.info = '  selected:\n    %s' % (
                    app.pages[launcher.app_select])
                if app.current != None:
                    del app.current
                    app.current = None
                if launcher.app_select == 1:
                    app.current = user()
                if launcher.app_select == 3:
                    app.current = user()

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
            app.ctrl.cycle()
            #time.sleep(0.1)


if __name__ == "__main__":
    app.run()
