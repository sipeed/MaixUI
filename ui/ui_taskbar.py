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


class taskbar:

    info, last = '', 0

    axp173 = AXP173()

    def time_draw():
        now = 45678 + time.ticks_ms() / 1000
        taskbar.info = time.localtime(int(now))
        ui.img.draw_string(60, 2, "%02u:%02u:%02u" % (
            taskbar.info[3], taskbar.info[4], taskbar.info[5]), scale=2, mono_space=1)

    def mem_draw():
        info = 'Rmnng %s KB' % str(gc.mem_free() / 1024)
        ui.img.draw_string(10, 2, info, scale=2)

    def battery_draw():
        #img = image.Image("res/icons/battery/0.jpg")
        #ui.img.draw_image(img, 10, 2, alpha=int(120))
        if taskbar.last + 3000 < time.ticks_ms():
            taskbar.last = time.ticks_ms()
            vbat_voltage = taskbar.axp173.getVbatVoltage()
            taskbar.info = "{0}".format(vbat_voltage, taskbar.axp173.is_charging())
        ui.img.draw_string(10, 2, taskbar.info, scale=2)

# config usb input limit 190ma
taskbar.axp173.enable_adc(True)
# 默认充电限制在 4.2V, 190mA 档位
taskbar.axp173.setEnterChargingControl(True)
taskbar.axp173.exten_output_enable()

if __name__ == "__main__":

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.bg_in_draw)
    @ui.warp_template(taskbar.battery_draw)
    def app_main():
        ui.display()
    import time
    while True:
        app_main()
        #time.sleep(0.5)
