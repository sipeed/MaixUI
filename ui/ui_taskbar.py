# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
import gc
import image

from ui_maix import ui

from pmu_axp173 import AXP173

levels = [4.13, 4.06, 3.98, 3.92, 3.87, 3.82, 3.79, 3.77, 3.74, 3.68, 3.45, 3.00]

class taskbar:

    now, info, last, img = '', '', 0, None

    axp173 = AXP173()

    def time_draw():
        now = 0 + time.ticks_ms() / 1000
        taskbar.now = time.localtime(int(now))
        ui.img.draw_string(30, 100, "%02u:%02u:%02u" % (
            taskbar.now[3], taskbar.now[4], taskbar.now[5]), color=(255, 255, 255), scale=3, mono_space=1)

    def mem_draw():
        info = 'Rmnng %s KB' % str(gc.mem_free() / 1024)
        ui.img.draw_string(10, 2, info, scale=2)

    def battery_draw():
        if taskbar.last + 3000 < time.ticks_ms():
            taskbar.last = time.ticks_ms()
            vbat_voltage = taskbar.axp173.getVbatVoltage() / 1000
            taskbar.info = "{0} V".format(vbat_voltage, taskbar.axp173.is_charging())
            if taskbar.img != None:
                del taskbar.img
            pos = int((4.2 - vbat_voltage) / 0.2)
            if pos < 6:
                tmp = "charge" if taskbar.axp173.is_charging() else "normal"
                taskbar.img = image.Image("res/icons/battery/{0} ({1}).jpg".format(tmp, 6 - pos))

        if taskbar.img != None:
            #ui.img.draw_rectangle((0,0,240,25), fill=True, color=(50, 50, 50))
            ui.img.draw_image(taskbar.img, 10, 2, alpha=int(255))
        ui.img.draw_string(100, 2, taskbar.info, scale=2, color=(255, 50, 50))

# config usb input limit 190ma
taskbar.axp173.enable_adc(True)
# 默认充电限制在 4.2V, 190mA 档位
taskbar.axp173.setEnterChargingControl(True)
taskbar.axp173.exten_output_enable()

if __name__ == "__main__":

    def tmp_draw():
        ui.img.draw_rectangle((0,0,240,240), fill=True, color=(75, 75, 75))

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(tmp_draw)
    @ui.warp_template(ui.anime_in_draw)
    @ui.warp_template(taskbar.time_draw)
    @ui.warp_template(taskbar.battery_draw)
    def app_main():
        ui.display()
    import time
    last = time.ticks_ms()
    while True:
        try:
            print(time.ticks_ms() - last)
            last = time.ticks_ms()
            app_main()
        except Exception as e:
            gc.collect()
            print(e)
