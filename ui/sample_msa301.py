# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

try:
    from core import agent
    from ui_maix import ui
    from ui_sample import sample_page
    from msa301 import MSA301, _MSA301_I2CADDR_DEFAULT
except ImportError:
    from lib.core import agent
    from ui.ui_maix import ui
    from ui.ui_sample import sample_page
    from driver.msa301 import MSA301, _MSA301_I2CADDR_DEFAULT

from fpioa_manager import fm
from machine import I2C

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


if __name__ == "__main__":
    from ui_taskbar import taskbar
    sample_page.add_sample(sample_msa301())

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(taskbar.battery_draw)
    @ui.warp_template(sample_page.sample_draw)
    def unit_test():
      ui.display()

    import time
    while True:
        unit_test()
        try:
            unit_test()
        except Exception as e:
            print(e)
