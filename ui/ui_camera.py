# This file is part of MaixUI
# Copyright (c) 2020 sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
import gc
import math
import random

from ui_maix import ui
import camera
import KPU as kpu
from face_recognition import FaceRecognition


class test_camera:

  info = 'Sensor Test'

  def info_draw():
    ui.img.draw_image(camera.obj.get_image(), 0, 0)
    ui.img.draw_string(40, 2, test_camera.info, color=(
        0, 255, 0), scale=2, mono_space=1)


class ai_camera:

    model = None

    def reload():
        FaceRecognition.free()
        FaceRecognition.load()
        ai_camera.model = FaceRecognition

    def ai_draw():
        tmp = camera.obj.get_image()
        if ai_camera.model and ai_camera.model.is_load:
            tmp.pix_to_ai()
            FaceRecognition.run_yolo2(tmp)
        ui.img.draw_image(tmp, 0, 0)


ai_camera.reload()

if __name__ == "__main__":

    def test_test_camera():

        @ui.warp_template(ui.blank_draw)
        @ui.warp_template(test_camera.info_draw)
        def app_main():
            ui.display()

        import time
        last = time.ticks_ms()
        while True:
            kpu.memtest()
            try:
                print(time.ticks_ms() - last)
                last = time.ticks_ms()
                app_main()
            except Exception as e:
                gc.collect()
                print(e)
            kpu.memtest()

    # test_test_camera()

    def test_ai_camera():

        @ui.warp_template(ui.blank_draw)
        @ui.warp_template(ai_camera.ai_draw)
        def app_main():
            ui.display()

        import time
        last = time.ticks_ms()
        while True:
            kpu.memtest()
            try:
                print(time.ticks_ms() - last)
                last = time.ticks_ms()
                app_main()
            except Exception as e:
                gc.collect()
                print(e)
            kpu.memtest()

    test_ai_camera()
