
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
        img1 = img.cut(80, 40, 160, 160).to_grayscale()
        #img.draw_image(img1, (0, 0))
        ui.canvas.draw_image(img1, (320, 0))
        #img1 = tmp
        #img1 = img1.to_grayscale(1)
        #tmp = img.resize(224, 224)
        #img1 = img.to_grayscale(1)  # convert to gray
        img2 = img1.cut(20, 20, 120, 120)  # resize to Minist input 28x28
        ui.canvas.draw_image(img2, (320 + 20, 160 + 20))

        a = img2.invert()  # invert picture as Minist need
        a = img2.strech_char(1)  # preprocessing pictures, eliminate dark corner
        img.draw_image(img2.resize(80, 80), (0, 0))  # display small 28x28 picture # alpha=25
        img2 = img2.resize(28, 28)
        a = img2.pix_to_ai()  # generate data for ai
        fmap = kpu.forward(Minist.task, img2)  # run neural network model
        plist = fmap[:]  # get result (10 digit's probability)
        pmax = max(plist)  # get max probability
        try:
            max_index = plist.index(pmax)  # get the digit
        except Exception as e:
            print(e)

        Minist.score = pmax
        Minist.result = max_index

        print(224, 0, "%d: %.3f" % (max_index, pmax))  # show result
        del img1, img2
        img.draw_rectangle(80, 40, 160, 160, thickness=2, color=(0, 255, 0))
        img.draw_rectangle(80 + 20, 40 + 20, 120, 120, thickness=2, color=(255, 0, 0))

        #img2 = img
        #img2 = img2.to_grayscale()  # convert to gray
        #img2 = img2.resize(28, 28)  # resize to mnist input 28x28
        #a = img2.invert()  # invert picture as mnist need
        ## a=img2.strech_char(1)			#preprocessing pictures, eliminate dark corner
        #img2x2 = img2.resize(28*2, 28*2)  # scale to display
        #a = ui.canvas.draw_image(img2x2, 0, 0)  # display small 28x28 picture
        #a = img2.pix_to_ai()  # generate data for ai
        ##watch conv0
        #a = kpu.set_layers(Minist.task, 1)
        #fmap = kpu.forward(Minist.task, img2)  # run neural network model
        #for i in range(0, 16):
            #tmp = kpu.fmap(fmap, i)
            #tmpx2 = tmp.resize(14*2, 14*2)  # scale to display
            #a = ui.canvas.draw_image(tmpx2, (i % 8)*14*2, 28*2+14*2*int(i/8))
        ##watch conv1
        #a = kpu.set_layers(Minist.task, 2)
        #fmap = kpu.forward(Minist.task, img2)  # run neural network model
        #for i in range(0, 32):
            #tmp = kpu.fmap(fmap, i)
            #tmpx2 = tmp.resize(7*2, 7*2)  # scale to display
            #a = ui.canvas.draw_image(
                #tmpx2, (i % 16)*7*2, 28*2+14*2*2+7*2*int(i/16))
        ##watch conv2
        #a = kpu.set_layers(Minist.task, 8)
        #fmap = kpu.forward(Minist.task, img2)  # run neural network model
        #for i in range(0, 10):
            #tmp = kpu.fmap(fmap, i)
            #tmpx2 = tmp.resize(4*2, 4*2)  # scale to display
            #a = ui.canvas.draw_image(tmpx2, i*4*2, 28*2+14*2*2+7*2*2)
        ##watch softmax
        #a = kpu.set_layers(Minist.task, 11)
        #fmap = kpu.forward(Minist.task, img2)
        #plist = fmap[:]
        #for i in range(0, 10):
            #cc = int(plist[i]*256)

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
            #ui.canvas.draw_string(0, ui.weight - 25, '%.2f:%s' %
                                  #(Minist.score, Minist.result), scale=2, color=(0, 255, 0))
            ui.display()

        import time
        last = time.ticks_ms()
        #while True:
        #try:
        #HowMany.load()
        #while True:
        #try:
        #print(time.ticks_ms() - last)
        #last = time.ticks_ms()
        #howmany()
        #except Exception as e:
        ## gc.collect()
        #print(e)
        #except KeyboardInterrupt as e:
        #HowMany.free()
        ##break
        #try:
        #MaybeIs.load()
        #while True:
        #try:
        #print(time.ticks_ms() - last)
        #last = time.ticks_ms()
        #maybe()
        #except Exception as e:
        ## gc.collect()
        #print(e)
        #except KeyboardInterrupt as e:
        #MaybeIs.free()
        ##break
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
