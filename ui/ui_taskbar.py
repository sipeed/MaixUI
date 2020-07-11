# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc

from ui_maix import ui

class taskbar:

  now = ''

  def time_draw():
    now = 45678 + time.ticks() / 1000
    taskbar.now = time.localtime(int(now))
    ui.img.draw_string(60, 2, "%02u:%02u:%02u" % (taskbar.now[3], taskbar.now[4], taskbar.now[5]), scale=2, mono_space=1)

  def mem_draw():
    info = 'Rmnng %s KB' % str(gc.mem_free() / 1024)
    ui.img.draw_string(10, 2, info, scale=2)

if __name__ == "__main__":

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(taskbar.time_draw)
    def app_main():
        ui.display()
    import time
    while True:
        app_main()
        #time.sleep(0.5)

