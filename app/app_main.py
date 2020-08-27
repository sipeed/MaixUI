# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc

from core import agent
from ui_canvas import ui, print_mem_free
from ui_system_info import system_info
#from ui_catch import catch
#from ui_taskbar import taskbar
from wdt import protect

class app:

    ctrl = agent()

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.grey_draw)
    @ui.warp_template(ui.bg_in_draw)
    @ui.warp_template(ui.anime_in_draw)
    #@ui.warp_template(ui.help_in_draw)
    #@ui.warp_template(taskbar.time_draw)
    #@ui.warp_template(taskbar.mem_draw)
    #@catch # need sipeed_button
    def draw():
        ui.display()

    def run():
        #app.ctrl.event(100, lambda *args: time.sleep(1))
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
                    # gc.collect()
                    print(e)

if __name__ == "__main__":
    # gc.collect()
    print_mem_free()
    app.run()
