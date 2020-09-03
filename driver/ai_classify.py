
from ui_canvas import ui
import camera
import KPU as kpu

# classify20

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

class HowMany():

    is_load = False

    task, things = None, None

    def load():
        if HowMany.is_load == False:
            #print(HowMany.load)
            HowMany.task = kpu.load(0x5C0000)
            #task = kpu.load("/sd/0x5C0000_20class.kmodel")
            kpu.init_yolo2(HowMany.task, 0.5, 0.3, 5, (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025))
            HowMany.is_load = True

    def work(img):

        HowMany.things = kpu.run_yolo2(HowMany.task, img)
        if HowMany.things:

            for pos in range(len(HowMany.things)):
                i = HowMany.things[pos]
                img.draw_rectangle(ui.weight - (i.x() + i.w()), i.y(), i.w(), i.h())
                img.draw_string(ui.weight - (i.x() + i.w()), i.y(), '%.2f:%s' % (i.value(), classes[i.classid()]), color=(0, 255, 0))

        return img

    def free():
        #print(HowMany.free)
        try:
            if HowMany.is_load:
                kpu.deinit(HowMany.task)
                HowMany.is_load = False
        except Exception as e:
            print(e)  # see py_kpu_deinit error will mp_raise_TypeError

class MaybeIs():

    is_load = False
    task, things, result = None, None, None

    def load():
        if MaybeIs.is_load == False:
            #print(MaybeIs.load)
            MaybeIs.task = kpu.load(0x5C0000)
            #task = kpu.load("/sd/0x5C0000_20class.kmodel")
            kpu.init_yolo2(MaybeIs.task, 0.5, 0.3, 5, (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025))
            MaybeIs.is_load = True

    def work(img):

        MaybeIs.things = kpu.run_yolo2(MaybeIs.task, img)
        if MaybeIs.things:

            value, obj = 0, None
            for k in range(len(MaybeIs.things)):
                if value < MaybeIs.things[k].value():
                    value, obj = MaybeIs.things[k].value(), MaybeIs.things[k]

            i = MaybeIs.things[k]
            MaybeIs.result = classes[i.classid()]
            img.draw_rectangle(ui.weight - (i.x() + i.w()), i.y(), i.w(), i.h())
            img.draw_string(ui.weight - (i.x() + i.w()), i.y(), '%.2f:%s' % (i.value(), classes[i.classid()]), color=(0, 255, 0))

        return img

    def free():
        #print(MaybeIs.free)
        try:
            if MaybeIs.is_load:
                kpu.deinit(MaybeIs.task)
                MaybeIs.is_load = False
        except Exception as e:
            print(e)  # see py_kpu_deinit error will mp_raise_TypeError


class MoblieNet():

    is_load = False
    task, things, result, score = None, None, None, None

    def load():
        if MoblieNet.is_load == False:
            #print(MoblieNet.load)
            MoblieNet.task = kpu.load(0x720000)
            #task = kpu.load("/sd/0x720000_mbnet75.kmodel")
            with open(os.getcwd() + '/res/labels.txt', 'r') as f:
            #with open('labels.txt', 'r') as f:
                MoblieNet.labels = f.readlines()
            MoblieNet.is_load = True

    def work(img):

        tmp = img.cut(48, 8, 224, 224)
        #tmp = img.resize(224, 224)
        img.draw_rectangle(48, 8, 224, 224, thickness=2, color=(0, 255, 0))
        tmp.pix_to_ai()
        MoblieNet.things = kpu.forward(MoblieNet.task, tmp)
        del tmp
        #print(MoblieNet.task, tmp)
        if MoblieNet.things:
            #print(MoblieNet.things)
            plist = MoblieNet.things[:]
            pmax = max(plist)
            max_index = plist.index(pmax)

            MoblieNet.score = pmax
            MoblieNet.result = MoblieNet.labels[max_index]

        return img

    def free():
        #print(MoblieNet.free)
        try:
            if MoblieNet.is_load:
                kpu.deinit(MoblieNet.task)
                MoblieNet.is_load = False
        except Exception as e:
            print(e)  # see py_kpu_deinit error will mp_raise_TypeError


if __name__ == "__main__":

    ui.height, ui.weight = 480, 320
    def test_ai_camera():

        @ui.warp_template(ui.blank_draw)
        def howmany():
            tmp = camera.obj.get_image()
            HowMany.work(tmp)
            ui.canvas.draw_image(tmp, 0, 0)
            ui.display()

        @ui.warp_template(ui.blank_draw)
        def maybe():
            tmp = camera.obj.get_image()
            MaybeIs.work(tmp)
            ui.canvas.draw_image(tmp, 0, 0)
            ui.display()

        @ui.warp_template(ui.blank_draw)
        def moblienet():
            tmp = camera.obj.get_image()
            MoblieNet.work(tmp)
            ui.canvas.draw_image(tmp, 0, 0)
            ui.canvas.draw_string(0, ui.weight - 25, '%.2f:%s' % (MoblieNet.score, MoblieNet.result.strip()), scale=2, color=(0, 255, 0))
            ui.display()

        import time
        last = time.ticks_ms()
        while True:
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
            MoblieNet.load()
            while True:
                try:
                    print(time.ticks_ms() - last)
                    last = time.ticks_ms()
                    moblienet()
                except KeyboardInterrupt as e:
                    MoblieNet.free()
                    ui.display()
                    break

    test_ai_camera()

