import os
import lcd, time
import sensor
from fpioa_manager import fm
from board import board_info
from Maix import GPIO
from framework import BaseApp, NeedRebootException


class CameraApp(BaseApp):

    '''Camera of class here
    face rocognition help info
    '''

    def __init__(self, system):
        #super(CameraApp, self).__init__(system)
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
        sensor.set_windowing((0, 0, 224, 224))  # MaixCube
        sensor.run(1)

        self.__initialized = True

    def on_back_pressed(self):
        raise NeedRebootException()

    # 在文件列表中循环
    def on_back_button_changed(self, state):
        print("Back 处理")
        self.get_system().navigate_back()
        pass

    def on_draw(self):
        if not self.__initialized:
            self.__lazy_init()
        try:
            while True:
                img = sensor.snapshot()  # Take an image from sensor
                img = img.rotation_corr(z_rotation=-90)
                lcd.display(img)
                # self.get_system().sayhello()
                # time.sleep(1)
                # home_button = self.get_system().home_button
                # TODO : 添加按键拍照, 录像,退出等功能
                # led_w = self.get_system().led_w
                # if home_button.value() == 0 and self.but_stu == 1:
                #     if led_w.value() == 1:
                #         led_w.value(0)
                #     else:
                #         led_w.value(1)
                #     self.but_stu = 0
                # if home_button.value() == 1 and self.but_stu == 0:
                #     self.but_stu = 1

        except KeyboardInterrupt:
            sys.exit()
