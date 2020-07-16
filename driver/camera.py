# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import sys
import time
import sensor
import lcd


class obj:

    is_init = False

    def init():
        sensor.reset(dual_buff=True)
        sensor.set_pixformat(sensor.YUV422)
        sensor.set_framesize(sensor.QVGA)
        sensor.set_hmirror(1)
        sensor.set_vflip(1)
        sensor.run(1)
        sensor.skip_frames()

    def get_image():
        if obj.is_init == False:
            obj.init()
            obj.is_init = True
        return sensor.snapshot()


if __name__ == "__main__":

    import KPU as kpu

    kpu.memtest()

    lcd.init(freq=15000000)

    print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')
    kpu.memtest()

    clock = time.clock()
    while(True):
        clock.tick()
        lcd.display(obj.get_image())
        print(clock.fps())
        print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')
        kpu.memtest()
