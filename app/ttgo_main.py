
import time
from core import agent
from ui_maix import ui
from ui_taskbar import taskbar
from ui_launcher import launcher
from ui_system_info import system_info
from button import ttgo_button

class app:

    index = 0
    ctrl = agent()
    btn = ttgo_button()

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
        ui.display()

    pages = ['Camera', 'Settings', 'Explorer', 'Statistics']

    def draw():
        if app.index != 0:
            if app.btn.home() == 2:
                app.index = 2 if app.index == 1 else 1
                system_info.info = '  selected:\n    %s' % (app.pages[launcher.app_select])

        elif app.btn.home() == 2:
                app.index = 1

        if app.index == 0:
            app.load()
        elif app.index == 1:
            launcher.btn.event()
            app.main()
        elif app.index == 2:
            app.user()

    def run():
        #app.ctrl.event(100, lambda *args: time.sleep(1))
        app.ctrl.event(10, app.draw)
        app.ctrl.event(10, app.btn.event)
        while True:
            app.ctrl.cycle()
            #time.sleep(0.1)

if __name__ == "__main__":
    app.run()
