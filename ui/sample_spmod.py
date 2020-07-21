# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

try:
    from core import agent
    from ui_maix import ui
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
        self.agent = agent()
        self.agent.event(1000, self.check)

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
                self.bme = BME280(self.i2c)
                self.config_bme = True
        if self.config_qmcx == False:
            if QMCX983_I2CADDR in self.i2c.scan():
                self.qmcx = QMCX983(self.i2c)
                self.config_qmcx = True

    def work(self):
        self.agent.cycle()
        ui.canvas.draw_string(30, 20, "BME280 & QMCX983", (127, 255, 0), scale=2)
        ui.canvas.draw_string(30, 60, "config_bme: %s" % (
            str)(self.config_bme), (255, 127, 0), scale=2)
        ui.canvas.draw_string(30, 100, "config_qmcx: %s" % (
            str)(self.config_qmcx), (255, 127, 0), scale=2)
        if self.config_bme:
            ui.canvas.draw_string(20, 150, str(
                self.bme.bmevalues()), (127, 255, 255), scale=2)
        if self.config_qmcx:
            ui.canvas.draw_string(20, 200, str(
                self.qmcx.read_xyz()), (127, 255, 255), scale=2)


if __name__ == "__main__":
    sample_page.add_sample(sample_spmod_test())

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(sample_page.sample_draw)
    def unit_test():
      ui.display()

    import time
    while True:
        try:
            unit_test()
        except Exception as e:
            print(e)
