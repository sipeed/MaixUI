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
    from bme280 import BME280, BME280_I2CADDR
    from qmcx983 import QMCX983, QMCX983_I2CADDR
except ImportError:
    from lib.core import agent
    from ui.ui_maix import ui
    from ui.ui_sample import sample_page
    from driver.bme280 import BME280, BME280_I2CADDR
    from driver.qmcx983 import QMCX983, QMCX983_I2CADDR

from machine import I2C

class sample_spmod_test():

    def __init__(self):
        self.is_load = False
        self.i2c = I2C(I2C.I2C0, freq=100*1000, scl=6, sda=7)
        self.config_bme = False
        self.config_qmcx = False
        self.cache_bme = (0, 0, 0)
        self.cache_qmcx = (0, 0, 0)
        self.agent = agent()
        self.agent.event(1000, self.check)
        self.agent.event(100, self.read_data)

    def load(self):
        if self.is_load == False:
            # i2c init()
            self.is_load = True

    def free(self):
        if self.is_load:
            # i2c deinit()
            self.is_load = False

    def check(self):
        if self.config_bme == False:
            if BME280_I2CADDR in self.i2c.scan():
                self.bme = BME280(i2c=self.i2c)
                self.config_bme = True
        if self.config_qmcx == False:
            if QMCX983_I2CADDR in self.i2c.scan():
                self.qmcx = QMCX983(i2c=self.i2c)
                self.config_qmcx = True

    def read_data(self):
        if self.config_bme:
            self.cache_bme = self.bme.read_compensated_data()
        if self.config_qmcx:
            self.cache_qmcx = self.qmcx.read_xyz()

    def bmevalues(data):
        t, p, h = data

        p = p // 256
        pi = p // 100
        pd = p - pi * 100
        p = pi + (pd / 100)

        hi = h // 1024
        hd = h * 100 // 1024 - hi * 100
        h = hi + (hd / 100)
        return "T{:.1f} C, P{:.2f} hPa, H{:.2f}%".format(t/100, p, h)
        #return "[] T={:.1f}\xb0C, P={:.2f}hPa, H={:.2f}%".format(t/100, p, h)

    def work(self):
        self.agent.parallel_cycle()
        ui.canvas.draw_string(30, 30, "BME280 & QMCX983", (127, 255, 0), scale=2)
        ui.canvas.draw_string(30, 60, "config_bme: %s" % (
            str)(self.config_bme), (255, 127, 0), scale=1)
        ui.canvas.draw_string(30, 80, "config_qmcx: %s" % (
            str)(self.config_qmcx), (255, 127, 0), scale=1)
        if self.config_bme:
            ui.canvas.draw_string(20, 100,
                sample_spmod_test.bmevalues(self.cache_bme), (127, 255, 255), scale=1)
        if self.config_qmcx:
            x, y, z = self.cache_qmcx
            ui.canvas.draw_string(20, 200, "({:0<3d}, {:0<3d}, {:0<3d})".format(int(x), int(y), int(z)), color=(127, 255, 255), scale=2)

            ui.canvas.draw_string(10, 130, "x", (255, 127, 0), scale=2)
            ui.canvas.draw_line(30, 140, int((x / 5) + 20), 140, color=(41, 131, 255))
            ui.canvas.draw_string(10, 150, "y", (255, 127, 0), scale=2)
            ui.canvas.draw_line(30, 160, int((y / 5) + 20), 160, color=(141, 31, 255))
            ui.canvas.draw_string(10, 170, "z", (255, 127, 0), scale=2)
            ui.canvas.draw_line(30, 180, int((z / 5) + 20), 180, color=(241, 131, 55))

if __name__ == "__main__":
    sample_page.add_sample(sample_spmod_test())

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(sample_page.sample_draw)
    def unit_test():
      ui.display()

    import time
    while True:
        unit_test()
