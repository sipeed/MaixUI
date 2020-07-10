import lcd, time
import KPU as kpu
import camera

class FaceRecognition():

    anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    is_load = False

    def load():
        if FaceRecognition.is_load == False:
            FaceRecognition.model = kpu.load(0x2C0000)  # Load Model File from Flash
            # Anchor data is for bbox, extracted from the training sets.
            kpu.init_yolo2(FaceRecognition.model, 0.5, 0.3, 5, FaceRecognition.anchor)
            FaceRecognition.is_load = True

    def run_yolo2(img):
            # Run the detection routine
            bbox = kpu.run_yolo2(FaceRecognition.model, img)
            if bbox:
                for i in bbox:
                    # print(i)
                    img.draw_rectangle(i.rect())

    def free():
        try:
            if FaceRecognition.is_load:
                tmp = kpu.deinit(FaceRecognition.model)
                FaceRecognition.is_load = False
        except Exception as e:
            print(e) # see py_kpu_deinit error will mp_raise_TypeError

if __name__ == "__main__":
    from ui_maix import ui
    import camera

    @ui.warp_template(ui.blank_draw) # first draw
    def app_main():
        # second draw
        tmp = camera.obj.get_image()
        tmp.pix_to_ai()
        FaceRecognition.run_yolo2(tmp)
        ui.img.draw_image(tmp, 0, 0)
        ui.display() # third display

    def unit_test():
        kpu.memtest()
        FaceRecognition.load()
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

        FaceRecognition.free()
        kpu.memtest()

    unit_test()
    unit_test()
