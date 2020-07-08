
import sys, time

from fpioa_manager import fm
from Maix import FPIOA, GPIO

BACK = 11
ENTER = 10
NEXT = 16

class cube_button:

    def __init__(self):
        self.home_last, self.next_last, self.back_last = 1, 1, 1
        self.cache = {
            'home':0,
            'next':0,
            'back':0,
        }

        fm.register(ENTER, fm.fpioa.GPIOHS10)
        self.home_button = GPIO(GPIO.GPIOHS10, GPIO.IN, GPIO.PULL_UP)
        if self.home_button.value() == 0:
            sys.exit()

        fm.register(BACK, fm.fpioa.GPIOHS11)
        self.back_button = GPIO(GPIO.GPIOHS11, GPIO.IN, GPIO.PULL_UP)

        fm.register(NEXT, fm.fpioa.GPIOHS16)
        self.next_button = GPIO(GPIO.GPIOHS16, GPIO.IN, GPIO.PULL_UP)

    def home(self):
        tmp, self.cache['home'] = self.cache['home'], 0
        return tmp

    def next(self):
        tmp, self.cache['next'] = self.cache['next'], 0
        return tmp

    def back(self):
        tmp, self.cache['back'] = self.cache['back'], 0
        return tmp

    def event(self):
        if self.home_button.value() == 0 and self.home_last == 1:
            self.cache['home'] = 1
            self.home_last = 0
        elif self.home_button.value() == 1 and self.home_last == 0:
            self.cache['home'] = 2
            self.home_last = 1

        if self.back_button.value() == 0 and self.back_last == 1:
            self.cache['back'] = 1
            self.back_last = 0
        elif self.back_button.value() == 1 and self.back_last == 0:
            self.cache['back'] = 2
            self.back_last = 1

        if self.next_button.value() == 0 and self.next_last == 1:
            self.cache['next'] = 1
            self.next_last = 0
        elif self.next_button.value() == 1 and self.next_last == 0:
            self.cache['next'] = 2
            self.next_last = 1


if __name__ == "__main__":
    tmp = cube_button()
    while True:
        tmp.event()
        time.sleep_ms(200)
        print(tmp.back(), tmp.home(), tmp.next())
        #print(tmp.home_button.value(), tmp.next_button.value(), tmp.back_button.value())
