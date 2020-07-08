
import time

from ui_maix import ui

class taskbar:

  now = ''

  def time_draw():
    now = 45678 + time.ticks() / 1000
    taskbar.now = time.localtime(int(now))
    ui.img.draw_string(60, 2, "%02u:%02u:%02u" % (taskbar.now[3], taskbar.now[4], taskbar.now[5]), scale=2, mono_space=1)

if __name__ == "__main__":

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(taskbar.time_draw)
    def app_main():
        ui.display()
    import time
    while True:
        app_main()
        #time.sleep(0.5)

