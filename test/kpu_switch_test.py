
import camera
import KPU as kpu

if __name__ == "__main__":

    import time
    last = time.ticks_ms()
    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
    while True:
        try:
            HowManyTask = kpu.load(0x5C0000)
            #task = kpu.load("/sd/0x5C0000_20class.kmodel")
            kpu.init_yolo2(HowManyTask, 0.5, 0.3, 5, (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025))
            while True:
                #print(time.ticks_ms() - last)
                last = time.ticks_ms()
                img = camera.obj.get_image()
                HowManyThings = kpu.run_yolo2(HowManyTask, img)
                if HowManyThings:

                    for pos in range(len(HowManyThings)):
                        i = HowManyThings[pos]
                        img.draw_rectangle(320 - (i.x() + i.w()), i.y(), i.w(), i.h())
                        img.draw_string(320 - (i.x() + i.w()), i.y(), '%.2f:%s' % (i.value(), classes[i.classid()]), color=(0, 255, 0))

                ## gc.collect() # have bug when reply 3
                lcd.display(img)
        except KeyboardInterrupt as e:
            pass
        finally:
            kpu.deinit(HowManyTask)
            #break
        try:
            FaceRecoModel = kpu.load(0x2C0000)
            kpu.init_yolo2(FaceRecoModel, 0.5, 0.3, 5, (1.889, 2.5245, 2.9465, 3.94056, 3.99987,
            5.3658, 5.155437, 6.92275, 6.718375, 9.01025))
            while True:
                #print(time.ticks_ms() - last)
                last = time.ticks_ms()
                img = camera.obj.get_image()
                img.pix_to_ai()
                # Run the detection routine
                FaceRecoBbox = kpu.run_yolo2(FaceRecoModel, img)
                if FaceRecoBbox:
                    for i in FaceRecoBbox:
                        # print(i)
                        img.draw_rectangle(i.rect())
                ## gc.collect() # have bug when reply 3
                lcd.display(img)
        except KeyboardInterrupt as e:
            pass
        finally:
            kpu.deinit(FaceRecoModel)
            #break
