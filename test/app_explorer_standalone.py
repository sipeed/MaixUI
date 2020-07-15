import os
import lcd
import image

from Maix import GPIO
from board import board_info
from fpioa_manager import fm

# import uos

S_IFDIR = 0o040000  # directory


# noinspection PyPep8Naming
def S_IFMT(mode):
    """Return the portion of the file's mode that describes the
    file type.
    """
    return mode & 0o170000


# noinspection PyPep8Naming
def S_ISDIR(mode):
    """Return True if mode is from a directory."""
    return S_IFMT(mode) == S_IFDIR


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class ExplorerApp:
    def __init__(self):
        self.current_offset = 0
        self.current_selected_index = 0
        self.__initialized = False
        self.is_dirty = True
        self.path = "/flash/"

    def __lazy_init(self):
        try:
            self.current_dir_files = os.listdir("/sd/")
            self.path = "/sd/"
        except Exception as e:
            print("Exception: " + str(e))
            self.current_dir_files = os.listdir("/flash/")
            self.path = "/flash/"

        print(self.current_dir_files)
        self.__initialized = True

    # 在文件列表中循环
    def on_top_button_changed(self, state):
        if state == "pressed":
            print("pressed")
            self.current_selected_index += 1
            if self.current_selected_index >= len(self.current_dir_files):
                self.current_selected_index = 0
            if self.current_selected_index >= 7:
                self.current_offset = self.current_selected_index - 6
            else:
                self.current_offset = 0
            print("current_selected=", self.current_selected_index,
                  "current_offset=", self.current_offset)
            self.is_dirty = True

    def on_draw(self):
        self.is_dirty = False
        if not self.__initialized:
            self.__lazy_init()
        x_offset = 4
        y_offset = 27
        path = "Path: " + self.path[0:20]
        # lcd.clear()
        img = image.Image(self.path + "res/images/bg.jpg")
        #img = image.Image()

        img.draw_string(x_offset, y_offset, path, lcd.WHITE, lcd.RED)
        y_offset += 18
        for i in range(self.current_offset, len(self.current_dir_files)):
            # gc.collect()
            file_name = self.current_dir_files[i]
            # print(file_name)
            try:
                f_stat = os.stat(self.path + file_name)
                if len(file_name) > 16:
                    file_name = file_name[0:14] + ".."
                if S_ISDIR(f_stat[0]):
                    file_name = file_name + '/'
                # gc.collect()
                file_readable_size = sizeof_fmt(f_stat[6])
                img.draw_string(lcd.width() - 50, y_offset,
                                file_readable_size, lcd.WHITE, lcd.BLUE)
            except Exception as e:
                print("-------------------->", e)
            is_current = self.current_selected_index == i
            line = "%s %d %s" % ("->" if is_current else "  ", i, file_name)
            img.draw_string(x_offset, y_offset, line, lcd.WHITE, lcd.RED)
            # gc.collect()
            y_offset += 18
            if y_offset > lcd.height():
                print(y_offset, lcd.height(), "y_offset > height(), break")
                break
        lcd.display(img)
# ----------------------

import os, lcd, image, sensor
import time
#lcd.init()
lcd.init()
lcd.rotation(2)  # Rotate the lcd 180deg
os.listdir("/flash")
os.listdir("")
img = image.Image("/sd/res/images/bg.jpg")
img = image.Image()

def test_irq(gpio, pin_num=None):
    value = gpio.value()
    time.sleep_ms(10)
    if (value == value & gpio.value()):
        state = "released" if value else "pressed"
        print("key", gpio, state)
        global app, key1, key2
        if gpio is key2:
            app.on_top_button_changed(state)



fm.register(10, fm.fpioa.GPIOHS21)
fm.register(11, fm.fpioa.GPIOHS22)
# fm.register(board_info.BUTTON_A, fm.fpioa.GPIOHS21, force=True)
key1 = GPIO(GPIO.GPIOHS21, GPIO.IN, GPIO.PULL_UP)
key2 = GPIO(GPIO.GPIOHS22, GPIO.IN, GPIO.PULL_UP)
key1.irq(test_irq, GPIO.IRQ_FALLING, GPIO.WAKEUP_NOT_SUPPORT, 7)
key2.irq(test_irq, GPIO.IRQ_FALLING, GPIO.WAKEUP_NOT_SUPPORT, 7)

app = ExplorerApp()

while True:
    if app.is_dirty:
        app.on_draw()
        # time.sleep_ms(1)
    else:
        time.sleep_ms(1000)
