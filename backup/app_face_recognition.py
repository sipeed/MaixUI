import lcd, time
from framework import BaseApp, NeedRebootException

import sensor
import KPU as kpu


class FaceRecognition(BaseApp):
    def __init__(self, system):
        super(FaceRecognition, self).__init__(system)
        self.__initialized = False

    def __lazy_init(self):
        err_counter = 0

        while 1:
            try:
                sensor.reset()  # Reset sensor may failed, let's try sometimes
                break
            except Exception:
                err_counter = err_counter + 1
                if err_counter == 20:
                    lcd.draw_string(lcd.width() // 2 - 100, lcd.height() // 2 - 4,
                                    "Error: Sensor Init Failed", lcd.WHITE, lcd.RED)
                time.sleep(0.1)
                continue
        print("progress 1 OK!")
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_framesize(sensor.QVGA)  # QVGA=320x240
        sensor.run(1)

        print("progress 2 OK!")
        self.task = kpu.load(0x300000)  # Load Model File from Flash
        anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987,
                  5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
        # Anchor data is for bbox, extracted from the training sets.
        print("progress 3 OK!")
        kpu.init_yolo2(self.task, 0.5, 0.3, 5, anchor)

        self.but_stu = 1

        self.__initialized = True

    def on_back_pressed(self):
        raise NeedRebootException()

    def on_draw(self):
        if not self.__initialized:
            self.__lazy_init()
        try:
            while True:
                img = sensor.snapshot()  # Take an image from sensor
                print("progress 4 OK!")
                # Run the detection routine
                bbox = kpu.run_yolo2(self.task, img)
                if bbox:
                    for i in bbox:
                        print(i)
                        img.draw_rectangle(i.rect())
                lcd.display(img)
                home_button = self.get_system().home_button
                # TODO
                led_w = self.get_system().led_w
                if home_button.value() == 0 and self.but_stu == 1:
                    if led_w.value() == 1:
                        led_w.value(0)
                    else:
                        led_w.value(1)
                    self.but_stu = 0
                if home_button.value() == 1 and self.but_stu == 0:
                    self.but_stu = 1

        except KeyboardInterrupt:
            a = kpu.deinit(task)
            sys.exit()
