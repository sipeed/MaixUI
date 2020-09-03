# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from ui_canvas import ui
import camera
import KPU as kpu


class Minist():

    is_load = False
    task, things, result, score = None, None, None, None

    def load():
        if Minist.is_load == False:
            #print(Minist.load)
            Minist.task = kpu.load(0x280000)
            #task = kpu.load("/sd/0x280000_Minist.kmodel")
            Minist.is_load = True

    def work(img):
        #tmp = image.Image(size=(160, 160))
        #tmp = tmp.to_grayscale()
        ui.canvas = ui.canvas.to_grayscale()
        bak = img.cut(100, 60, 120, 120).to_grayscale()
        #img.draw_image(tmp, (0, 0))
        ui.canvas.draw_image(bak, (320 + 20, 0 + 20))
        #img1 = tmp
        #img1 = img1.to_grayscale(1)
        #tmp = img.resize(224, 224)
        #img1 = img.to_grayscale(1)  # convert to gray
        #tmp = img1.cut(20, 20, 120, 120)  # resize to Minist input 28x28
        #ui.canvas.draw_image(tmp, (320 + 20, 160 + 20))

        a = bak.invert()  # invert picture as Minist need
        a = bak.strech_char(1)  # preprocessing pictures, eliminate dark corner
        img.draw_image(bak.resize(80, 80), (0, 0))  # display small 28x28 picture # alpha=25
        bak = bak.resize(28, 28)
        a = bak.pix_to_ai()  # generate data for ai
        fmap = kpu.forward(Minist.task, bak)  # run neural network model
        plist = fmap[:]  # get result (10 digit's probability)
        pmax = max(plist)  # get max probability
        try:
            max_index = plist.index(pmax)  # get the digit
        except Exception as e:
            print(e)

        Minist.score = pmax
        Minist.result = max_index

        #ui.canvas.draw_string(0, 300, "%d: %.3f" % (max_index, pmax), scale=2)  # show result

        img.draw_rectangle(80, 40, 160, 160, thickness=2, color=(0, 255, 0))
        img.draw_rectangle(80 + 20, 40 + 20, 120, 120, thickness=2, color=(255, 0, 0))

        if ui.weight > 240:

            size = 28*2
            x, y = 5, int(240) + 5 - size

            #watch conv0
            a = kpu.set_layers(Minist.task, 1)
            fmap = kpu.forward(Minist.task, bak)  # run neural network model
            for i in range(0, 16):
                tmp = kpu.fmap(fmap, i)
                tmpx2 = tmp.resize(14*2, 14*2)  # scale to display
                a = ui.canvas.draw_image(tmpx2, (i % 8)*14*2 + x, y + size+14*2*int(i/8))
            x, y = x + 10 + size*4, y + 5 - size
            #watch conv1
            a = kpu.set_layers(Minist.task, 2)
            fmap = kpu.forward(Minist.task, bak)  # run neural network model
            for i in range(0, 32):
                tmp = kpu.fmap(fmap, i)
                tmpx2 = tmp.resize(7*2, 7*2)  # scale to display
                a = ui.canvas.draw_image(
                    tmpx2, (i % 16)*7*2 + x, y + size+14*2*2+7*2*int(i/16))
            x, y = x + 15, y + 10
            #watch conv2
            a = kpu.set_layers(Minist.task, 8)
            fmap = kpu.forward(Minist.task, bak)  # run neural network model
            for i in range(0, 10):
                tmp = kpu.fmap(fmap, i)
                tmpx2 = tmp.resize(4*4, 4*4)  # scale to display
                a = ui.canvas.draw_image(tmpx2, i*4*4 + x + i * 5, y + size+14*2*2+7*2*2)

            #watch softmax
            a = kpu.set_layers(Minist.task, 11)
            fmap = kpu.forward(Minist.task, bak)
            plist = fmap[:]
            for i in range(0, 10):
                cc = int(plist[i]*256)
                ui.canvas.draw_string(i*4*4 + x + 3 + i * 5, y + 20 + size+14*2*2+7*2*2, '%.0f' % (plist[i] * 100), scale=1, color=(255, 255, 255))
                #print(i, cc)

        del bak

        return img

    def free():
        #print(Minist.free)
        try:
            if Minist.is_load:
                kpu.deinit(Minist.task)
                Minist.is_load = False
        except Exception as e:
            print(e)  # see py_kpu_deinit error will mp_raise_TypeError


if __name__ == "__main__":

    ui.height, ui.weight = 480, 320
    def test_ai_camera():

        @ui.warp_template(ui.blank_draw)
        def test_minist():
            tmp = camera.obj.get_image()
            Minist.work(tmp)
            ui.canvas.draw_image(tmp, 0, 0)
            ui.canvas.draw_string(5, ui.weight - 20, 'minist result > %d : %.2f' %
                                  (Minist.result, Minist.score), scale=2, color=(255, 255, 255))
            ui.display()

        import time
        last = time.ticks_ms()
        Minist.load()
        while True:
            try:
                print(time.ticks_ms() - last)
                last = time.ticks_ms()
                test_minist()
            except KeyboardInterrupt as e:
                Minist.free()
                ui.display()
                break

    test_ai_camera()
