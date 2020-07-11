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

        if sample_page.btn.back() == 1:
            sample_page.index -= 1
            sample_page.replace = True
        elif sample_page.btn.next() == 1:
            sample_page.index += 1
            sample_page.replace = True
        sample_page.index = sample_page.index % len(sample_page.samples)

        if sample_page.replace:
            sample_page.reload()

        if sample_page.case:
            sample_page.case.work()

if __name__ == "__main__":

    class case1():

        def __init__(self):
            self.is_load = False

        def load(self):
            if self.is_load == False:
                #print(case.load)
                self.is_load = True

        def work(self):
            #print(case.work)
            ui.img.draw_string(20, 200, 'mem free %d kb' % (gc.mem_free() / 1024), (127, 255, 255), scale=2)

            ui.img.draw_line(0,0, 240,240,color=(255,0,0))

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
            ui.img.draw_string(20, 200, 'heap free %d kb' % (utils.heap_free() / 1024), (127, 255, 255), scale=2)

        def free(self):
            if self.is_load:
                #print(sample.free)
                self.is_load = False

    sample_page.add_sample(case1())
    sample_page.add_sample(case2())

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
