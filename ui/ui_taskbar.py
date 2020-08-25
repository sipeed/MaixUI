# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
import gc
import image

try:
    from core import agent
    from ui_canvas import ui
except ImportError:
    from lib.core import agent
    from ui.ui_canvas import ui

#levels = [4.13, 4.06, 3.98, 3.92, 3.87,
          #3.82, 3.79, 3.77, 3.74, 3.68, 3.45, 3.00]

class taskbar:

    charge = b"\x00\x01\x03\x07\x0F\x1E\x3F\x7F\xFF\x00\x00\x01\x01\x03\x03\x06\xC0\x80\x80\x00\x00\x00\xFF\xFE\xFC\x78\xF0\xE0\xC0\x80\x00\x00"
    normal = b"\x00\x00\x00\x7F\xC0\x80\x80\x80\x80\x80\x80\xC0\x7F\x00\x00\x00\x00\x00\x00\xFC\x06\x02\x03\x01\x01\x03\x02\x06\xFC\x00\x00\x00"

    now, info, last, sync = '', '', 0, None

    power = None
    ctrl = agent()

    def init(power):
        taskbar.power = power
        ## config usb input limit 190ma
        #taskbar.axp173.enable_adc(True)
        ## 默认充电限制在 4.2V, 190mA 档位
        #taskbar.axp173.setEnterChargingControl(True)
        #taskbar.axp173.exten_output_enable()
        taskbar.ctrl.event(3000, taskbar.battery_sync)

    def time_draw():
        now = 0 + time.ticks_ms() / 1000
        taskbar.now = time.localtime(int(now))
        ui.canvas.draw_string(int((ui.height) / 2) - 60, 2, "%02u:%02u:%02u" % (
            taskbar.now[3], taskbar.now[4], taskbar.now[5]), color=(255, 255, 255), scale=2, mono_space=1)

    pos = 0

    def mem_draw():
        info = 'Rmnng %s KB' % str(gc.mem_free() / 1024)
        ui.canvas.draw_string(10, 2, info, scale=2)

    def battery_sync():
        try:
            vbat_voltage = taskbar.power.getVbatVoltage() / 1000
            vbat_value = int((vbat_voltage - 3.12) * 100)
            taskbar.sync = (taskbar.power.is_charging(), vbat_value)
        except Exception as e:
            gc.collect()
            print(e)

    def battery_draw():
        taskbar.ctrl.cycle()
        if taskbar.sync != None:
            #ui.canvas.draw_rectangle((0,0,240,25), fill=True, color=(50, 50, 50))
            #ui.canvas.draw_image(taskbar.img, ui.height - 32, 2, alpha=int(255))
            charge, value = taskbar.sync
            ui.canvas.draw_font(ui.height - 40, 0, 16, 16, taskbar.normal, scale=2, color=(300 - value * 3, value * 2, 50))
            if charge == True:
                ui.canvas.draw_font(ui.height - 60, 8, 16, 16, taskbar.charge, scale=1, color=(300 - value * 3, value * 2, 50))

            #print('{0:>2d}%'.format(value))
            ui.canvas.draw_string(ui.height - 32, 10, '{0:>2d}%'.format(value), scale=1, color=(255,255,255))

        #ui.canvas.draw_string(10, 1, taskbar.info,
                              #scale=2, color=(50, 255, 50))

#taskbar.init()

if __name__ == "__main__":

    from machine import I2C
    from fpioa_manager import fm
    fm.register(24,fm.fpioa.I2C1_SCLK, force=True)
    fm.register(27,fm.fpioa.I2C1_SDA, force=True)
    from pmu_axp173 import AXP173

    i2c = I2C(I2C.I2C1, freq=400*1000)
    axp173 = AXP173(i2c_dev=i2c)
    axp173.enable_adc(True)
    # 默认充电限制在 4.2V, 190mA 档位
    axp173.setEnterChargingControl(True)
    axp173.exten_output_enable()
    # amigo sensor config.
    axp173.writeREG(0x27, 0x20)
    axp173.writeREG(0x28, 0x0C)

    taskbar.init(axp173)

    ui.height, ui.weight = 480, 320

    #def tmp_draw():
        #ui.canvas.draw_rectangle(
            #(0, 0, 240, 240), fill=True, color=(75, 75, 75))

    @ui.warp_template(ui.blank_draw)
    #@ui.warp_template(tmp_draw)
    @ui.warp_template(ui.anime_in_draw)
    @ui.warp_template(taskbar.time_draw)
    @ui.warp_template(taskbar.battery_draw)
    def app_main():
        ui.display()
    import time
    last = time.ticks_ms()
    while True:
        #print(time.ticks_ms() - last)
        last = time.ticks_ms()
        app_main()
        continue
        try:
            #print(time.ticks_ms() - last)
            last = time.ticks_ms()
            app_main()
        except Exception as e:
            gc.collect()
            print(e)
