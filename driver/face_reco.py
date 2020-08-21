# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import lcd
import time
import KPU as kpu

from Maix import utils

try:
    import camera
except ImportError:
    import driver.camera as camera


class FaceReco():

    anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987,
              5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    is_load = False
    bbox = None

    def load():
        if FaceReco.is_load == False:
            FaceReco.model = kpu.load(0x2C0000)  # Load Model File from Flash
            # Anchor data is for bbox, extracted from the training sets.
            kpu.init_yolo2(FaceReco.model, 0.5, 0.3, 5, FaceReco.anchor)
            FaceReco.is_load = True

    def work(img):
        img.pix_to_ai()
        # Run the detection routine
        FaceReco.bbox = kpu.run_yolo2(FaceReco.model, img)
        if FaceReco.bbox:
            for i in FaceReco.bbox:
                # print(i)
                img.draw_rectangle(i.rect())

        img.draw_string(10, 2, 'FaceReco free %d kb' % (
            utils.heap_free() / 1024), (127, 255, 255), scale=2)

    def free():
        try:
            if FaceReco.is_load:
                tmp = kpu.deinit(FaceReco.model)
                FaceReco.is_load = False
        except Exception as e:
            print(e)  # see py_kpu_deinit error will mp_raise_TypeError


if __name__ == "__main__":
    try:
        from ui_canvas import ui
    except ImportError:
        from ui.ui_canvas import ui


    @ui.warp_template(ui.blank_draw)  # first draw
    def app_main():
        # second draw
        tmp = camera.obj.get_image()
        FaceReco.work(tmp)
        ui.canvas.draw_image(tmp, 0, 0)
        ui.display()  # third display

    def unit_test():
        kpu.memtest()
        FaceReco.load()
        kpu.memtest()
        import time
        last = time.ticks_ms()
        i = 0
        while i < 10:
            i += 1
            print(i)
            try:
                #print(time.ticks_ms() - last)
                last = time.ticks_ms()
                app_main()
            except Exception as e:
                gc.collect()
                print(e)

        FaceReco.free()
        kpu.memtest()

    unit_test()
    unit_test()
