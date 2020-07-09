# This file is part of MaixUI
# Copyright (c) 2020 sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import sys, time
import sensor, lcd
import KPU as kpu

def camera_init():
    sensor.reset()
    sensor.set_pixformat(sensor.YUV422)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)
    sensor.skip_frames()

    sensor.set_hmirror(1)
    sensor.set_vflip(1)

def get_image():

    return sensor.snapshot()

try:
    camera_init()
except Exception as e:
    time.sleep(1)
    camera_init()

if __name__ == "__main__":

    kpu.memtest()
    
    lcd.init(freq=15000000)

    print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')
    kpu.memtest()

    clock = time.clock()
    while(True):
        clock.tick()
        lcd.display(get_image())
        print(clock.fps())
        print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')
        kpu.memtest()
