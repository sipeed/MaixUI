# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
import gc
import math
import random

try:
    from ui.ui_maix import ui
    from driver.button import cube_button
except ImportError:
    from ui_maix import ui
    from button import cube_button


class sample_page():

    index, case, samples = 0, None, []
    btn, replace = cube_button(), False

    def add_sample(s):
        sample_page.samples.insert(0, s)
        sample_page.case = s

    def reload():
        if sample_page.case:
            sample_page.case.free()
            sample_page.case = sample_page.samples[sample_page.index]
            sample_page.case.load()

    def sample_draw():
        sample_page.btn.event()
        sample_page.replace = False

        if sample_page.btn.back() == 2:
            sample_page.index -= 1
            sample_page.replace = True
        elif sample_page.btn.next() == 2:
            sample_page.index += 1
            sample_page.replace = True
        sample_page.index = sample_page.index % len(sample_page.samples)

        if sample_page.replace:
            sample_page.reload()

        if sample_page.case:
            sample_page.case.work()

    def add_demo():

        class case1():

            def __init__(self):
                self.is_load = False

            def load(self):
                if self.is_load == False:
                    #print(case.load)
                    self.is_load = True

            def work(self):
                #print(case.work)
                ui.canvas.draw_string(20, 200, 'mem free %d kb' % (
                    gc.mem_free() / 1024), (127, 255, 255), scale=2)

                ui.canvas.draw_rectangle(
                    (80, 80, 30, 30), color=(255, 220, 123))
                ui.canvas.draw_circle((150, 140, 30), color=(255, 63, 123))
                ui.canvas.draw_cross((150, 40), color=(255, 136, 210))
                ui.canvas.draw_arrow((150, 150, 20, 170), color=(236, 198, 255))
                ui.canvas.draw_line(20, 20, 200, 200, color=(41, 131, 255))
                ui.canvas.draw_ellipse(120, 120, 80, 60, 15, color=(
                    51, 251, 123), thickness=2, fill=False)

            def free(self):
                if self.is_load:
                    #print(sample.free)
                    self.is_load = False

        class case2():

            def __init__(self):
                self.is_load = False

            def load(self):
                if self.is_load == False:
                    #print(case.load)
                    self.is_load = True

            def work(self):
                #print(self.work)
                from Maix import utils
                ui.canvas.draw_string(20, 200, 'heap free %d kb' % (
                    utils.heap_free() / 1024), (127, 255, 255), scale=2)

                wai = b'\x00\x00\x04\x08\x08\x0F\x11\x11\x29\x26\x42\x04\x04\x08\x10\x20\x00\x00\x20\x20\x20\xA0\x20\x38\x24\x22\x20\x20\x20\x20\x20\x20'

                ui.canvas.draw_font(50, 100, 16, 16, wai,
                                    scale=1, color=(255, 0, 0))
                ui.canvas.draw_font(100, 100, 16, 16, wai,
                                    scale=2, color=(0, 255, 0))
                ui.canvas.draw_font(150, 50, 16, 16, wai,
                                    scale=3, color=(0, 0, 255))

            def free(self):
                if self.is_load:
                    #print(sample.free)
                    self.is_load = False

        sample_page.add_sample(case1())
        sample_page.add_sample(case2())


if __name__ == "__main__":

    sample_page.add_demo()

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(sample_page.sample_draw)
    def app_main():
        ui.display()

    import time
    last = time.ticks_ms()
    while True:
        print(time.ticks_ms() - last)
        last = time.ticks_ms()
        app_main()
        #try:
        #print(time.ticks_ms() - last)
        #last = time.ticks_ms()
        #app_main()
        #except Exception as e:
        #gc.collect()
        #print(e)
