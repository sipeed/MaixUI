# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import lcd
import time
import image
import gc
import KPU as kpu

from Maix import utils

try:
    import camera
    from button import sipeed_button, button_io
    from ui_canvas import ui
except ImportError:
    import driver.camera as camera
    from driver.button import sipeed_button, button_io
    from ui.ui_canvas import ui

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987,
          5.3658, 5.155437, 6.92275, 6.718375, 9.01025)


class FaceDetect():

    is_load = False
    bbox = None

    def load():
        if FaceDetect.is_load == False:
            FaceDetect.model = kpu.load(0x2C0000)  # Load Model File from Flash
            # Anchor data is for bbox, extracted from the training sets.
            kpu.init_yolo2(FaceDetect.model, 0.5, 0.3, 5, anchor)
            FaceDetect.is_load = True

    def work(img):
        img.pix_to_ai()
        # Run the detection routine
        FaceDetect.bbox = kpu.run_yolo2(FaceDetect.model, img)
        if FaceDetect.bbox:
            for i in FaceDetect.bbox:
                # print(i)
                img.draw_rectangle(i.rect())

        # img.draw_string(10, 2, 'FaceDetect free %d kb' % (
        #     utils.heap_free() / 1024), (127, 255, 255), scale=2)

    def free():
        try:
            if FaceDetect.is_load:
                tmp = kpu.deinit(FaceDetect.model)
                FaceDetect.is_load = False
        except Exception as e:
            print(e)  # see py_kpu_deinit error will mp_raise_TypeError


class FaceReco():

    is_load = False
    img_face = None
    task_fd, task_ld, task_fe = None, None, None
    record_ftr = []
    record_ftrs = []
    btn = sipeed_button()
    names = ['Mr.1', 'Mr.2', 'Mr.3', 'Mr.4', 'Mr.5', 'Mr.6', 'Mr.7', 'Mr.8']
    dst_point = [(44, 59), (84, 59), (64, 82), (47, 105),
                 (81, 105)]  # standard face key point position
    start_processing = False

    def set_key_state(*_):
        FaceReco.start_processing = True

    def load():
        if FaceReco.is_load == False:
            FaceReco.task_fd = kpu.load(0x2C0000)
            FaceReco.task_ld = kpu.load(0x580000)
            FaceReco.task_fe = kpu.load(0x340000)

            a = kpu.init_yolo2(FaceReco.task_fd, 0.5, 0.3, 5, anchor)

            FaceReco.img_face = image.Image(size=(128, 128))
            a = FaceReco.img_face.pix_to_ai()

            FaceReco.start_processing = False

            from Maix import GPIO
            button_io.home_button.irq(
                FaceReco.set_key_state, GPIO.IRQ_RISING, GPIO.WAKEUP_NOT_SUPPORT)

            FaceReco.is_load = True

    def work(img):
        img.pix_to_ai()

        code = kpu.run_yolo2(FaceReco.task_fd, img)
        if code:
            #for i in code:
            start = 0
            for pos in range(len(code)):
                i = code[pos]
                #print(i)
                # Cut face and resize to 128x128
                a = img.draw_rectangle(i.x(), i.y(), i.w(), i.h())
                face_cut = img.cut(i.x(), i.y(), i.w(), i.h())
                face_cut_128 = face_cut.resize(128, 128)
                a = face_cut_128.pix_to_ai()

                #a = ui.canvas.draw_image(face_cut, (320,0))
                #print(i)

                # Landmark for face 5 points
                fmap = kpu.forward(FaceReco.task_ld, face_cut_128)
                plist = fmap[:]
                le = (int(i.x() + plist[0]*i.w() - 5),
                      int(i.y() + plist[1]*i.h()))
                re = (int(i.x() + plist[2]*i.w()), int(i.y() + plist[3]*i.h()))
                nose = (int(i.x() + plist[4]*i.w()),
                        int(i.y() + plist[5]*i.h()))
                lm = (int(i.x() + plist[6]*i.w()), int(i.y() + plist[7]*i.h()))
                rm = (int(i.x() + plist[8]*i.w()), int(i.y() + plist[9]*i.h()))
                #print(le, re, nose, lm, rm)
                a = img.draw_circle(int(le[0]), int(le[1]), 2)
                a = img.draw_circle(int(re[0]), int(re[1]), 2)
                a = img.draw_circle(int(nose[0]), int(nose[1]), 2)
                a = img.draw_circle(int(lm[0]), int(lm[1]), 2)
                a = img.draw_circle(int(rm[0]), int(rm[1]), 2)
                # align face to standard position
                src_point = [le, re, nose, lm, rm]
                T = image.get_affine_transform(src_point, FaceReco.dst_point)
                a = image.warp_affine_ai(img, FaceReco.img_face, T)
                a = FaceReco.img_face.ai_to_pix()
                #a = ui.canvas.draw_image(FaceReco.img_face, (320,128))

                if ui.height > 240:
                    gc.collect()
                    tmp = face_cut_128.resize(80, 80)
                    #a = ui.canvas.draw_image(face_cut_128, (start, 240))
                    ui.canvas.draw_image(
                        tmp, 320 + int((pos % 2)*80), int((pos // 2)*80))
                    del(tmp)
                    #start = start + 80
                del(face_cut_128)

                # calculate face feature vector
                fmap = kpu.forward(FaceReco.task_fe, FaceReco.img_face)
                feature = kpu.face_encode(fmap[:])
                reg_flag = False
                scores = []
                for j in range(len(FaceReco.record_ftrs)):
                   score = kpu.face_compare(FaceReco.record_ftrs[j], feature)
                   scores.append(score)
                max_score = 0
                index = 0
                for k in range(len(scores)):
                   if max_score < scores[k]:
                       max_score = scores[k]
                       index = k
                if max_score > 85:
                    a = img.draw_string(i.x(), i.y(), ("%s:%2.1f" % (
                        FaceReco.names[index], max_score)), color=(0, 255, 0), scale=2)
                    if ui.height > 240:
                        a = ui.canvas.draw_string(100 * (pos % 3), 240 + 30 * (pos // 3), ("%s :%2.1f" % (
                            FaceReco.names[index], max_score)), color=(0, 255, 0), scale=2)
                else:
                    a = img.draw_string(i.x(), i.y(), ("X:%2.1f" % (
                        max_score)), color=(255, 0, 0), scale=2)
                    if ui.height > 240:
                        a = ui.canvas.draw_string(100 * (pos % 3), 240 + 30 * (pos // 3), ("X :%2.1f" % (
                            max_score)), color=(255, 0, 0), scale=2)

                if FaceReco.start_processing:
                    FaceReco.record_ftr = feature
                    if len(FaceReco.record_ftrs) == len(FaceReco.names):
                        FaceReco.record_ftrs = []
                    FaceReco.record_ftrs.append(FaceReco.record_ftr)
                    FaceReco.start_processing = False

        # img.draw_string(10, 2, 'FaceReco free %d kb' % (
        #     utils.heap_free() / 1024), (127, 255, 255), scale=2)

    def free():
        try:
            if FaceReco.is_load:
                tmp = kpu.deinit(FaceReco.task_fd)
                tmp = kpu.deinit(FaceReco.task_ld)
                tmp = kpu.deinit(FaceReco.task_fe)
                #t, FaceReco.task_fd = FaceReco.task_fd, None
                #del t
                #t, FaceReco.task_ld = FaceReco.task_ld, None
                #del t
                #t, FaceReco.task_fe = FaceReco.task_fe, None
                #del t
                t, FaceReco.img_face = FaceReco.img_face, None
                del t

                FaceReco.record_ftr = []
                FaceReco.record_ftrs = []

                button_io.home_button.disirq()
                FaceReco.start_processing = False

                FaceReco.is_load = False
                gc.collect()
        except Exception as e:
            print(e)  # see py_kpu_deinit error will mp_raise_TypeError


if __name__ == "__main__":
    try:
        from ui_canvas import ui
    except ImportError:
        from ui.ui_canvas import ui

    ui.height, ui.weight = 480, 320
    # button_io.config(10, 11, 16) # cube
    button_io.config(23, 31, 20)  # amigo 3.8M 750*1024

    @ui.warp_template(ui.blank_draw)  # first draw
    def app_main():
        # second draw
        tmp = camera.obj.get_image()
        FaceReco.work(tmp)
        ui.canvas.draw_image(tmp, 0, 0)
        ui.display()  # third display

    def unit_test():
        gc.collect()
        kpu.memtest()
        FaceReco.load()
        kpu.memtest()
        import time
        last = time.ticks_ms()
        i = 0
        while i < 20:
            i += 1
            #print(i)
            try:
                #kpu.memtest()
                gc.collect()
                print(time.ticks_ms() - last)
                last = time.ticks_ms()
                app_main()
            except Exception as e:
                #
                print(e)
        FaceReco.free()
        gc.collect()

        #kpu.memtest()
        #test = kpu.load(0x5C0000)
        #kpu.memtest()
        #tmp = kpu.deinit(test)
        #del test
        #kpu.memtest()

    unit_test()
    unit_test()
    unit_test()
    #unit_test()
