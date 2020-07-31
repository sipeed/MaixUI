# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math, random

from fpioa_manager import fm
from machine import I2C

from ui_canvas import ui
from ui_sample import sample_page
from core import agent

from led import cube_led
from es8374 import ES8374
from button import cube_button
from pmu_axp173 import AXP173
from msa301 import MSA301, _MSA301_I2CADDR_DEFAULT
from shtxx import SHT3x, SHT3x_ADDR, SHT31_ADDR
from bme280 import BME280, BME280_I2CADDR
from qmcx983 import QMCX983, QMCX983_I2CADDR

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

    class sample_msa301():

        def __init__(self):
            self.is_load = False
            self.i2c = I2C(I2C.I2C1, freq=100*1000, sda=31, scl=30)
            #fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
            #fm.register(31, fm.fpioa.I2C1_SDA, force=True)
            self.isconnected = False
            self.agent = agent()
            self.agent.event(500, self.check)
            self.tapped = False
            self.acceleration = (0, 0, 0)

        def load(self):
            if self.is_load == False:
                # i2c init()
                fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
                fm.register(31, fm.fpioa.I2C1_SDA, force=True)
                self.is_load = True

        def free(self):
            if self.is_load:
                # i2c deinit()
                self.is_load = False

        def check(self):
            if self.isconnected == False:
                if _MSA301_I2CADDR_DEFAULT in self.i2c.scan():
                    self.msa301 = MSA301(self.i2c)
                    self.isconnected = True
            else:
                self.tapped = self.msa301.tapped
                self.acceleration = self.msa301.acceleration

        def work(self):
            self.agent.cycle()
            ui.canvas.draw_string(30, 30, "Test MSA301", (127, 127, 255), scale=3)
            ui.canvas.draw_string(30, 70, "isconnected: %s" % (
                str)(self.isconnected), (255, 127, 0), scale=2)
            if self.isconnected:
                ui.canvas.draw_string(30, 120, "tapped: %s" % (
                    str)(self.tapped), (0, 214, 126), scale=2)

                ui.canvas.draw_string(10, 140, "x", (255, 0, 0), scale=2)
                ui.canvas.draw_line(120, 150, 120 + int(self.acceleration[0] * 8), 150, color=(41, 131, 255))
                ui.canvas.draw_string(10, 160, "y", (0, 255, 0), scale=2)
                ui.canvas.draw_line(120, 170, 120 + int(self.acceleration[1] * 8), 170, color=(141, 31, 255))
                ui.canvas.draw_string(10, 180, "z", (0, 0, 255), scale=2)
                ui.canvas.draw_line(120, 190, 120 + int(self.acceleration[2] * 8), 190, color=(241, 131, 55))

                ui.canvas.draw_string(40, 210,
                    str(("%-02.2f %-02.2f %-02.2f" % self.acceleration)), (127, 255, 255), scale=2)

    class case3():

        def __init__(self):
            self.is_load = False

        def load(self):
            if self.is_load == False:
                #print(case.load)
                self.is_load = True

        def work(self):

            #print(self.work)
            from Maix import utils
            ui.canvas.draw_string(20, 200, 'test free %d kb' % (
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
    #sample_page.add_sample(sample_msa301())
    sample_page.add_sample(case3())

    sample_page.btn.config(10, 11, 16)

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
        try:
            print(time.ticks_ms() - last)
            last = time.ticks_ms()
            app_main()
        except Exception as e:
            gc.collect()
            print(e)
