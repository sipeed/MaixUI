# This file is part of MaixUI
# Copyright (c) 2020 sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math, random

from ui_maix import ui
import camera
import KPU as kpu

class test_camera:

  info = 'Sensor Test'

  def info_draw():
    ui.img.draw_image(camera.obj.get_image(), 0, 0) # 50ms
    ui.img.draw_string(40, 2, test_camera.info, color=(0, 255, 0), scale=2, mono_space=1)

if __name__ == "__main__":

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(test_camera.info_draw)
    def app_main():
        ui.display()

    import time
    last = time.ticks_ms()
    while True:
        kpu.memtest()
        try:
            print(time.ticks_ms() - last)
            last = time.ticks_ms()
            app_main()
        except Exception as e:
            gc.collect()
            print(e)
        kpu.memtest()
