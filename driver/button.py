# This file is part of MaixUI
# Copyright (c) 2020 sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import sys, time

from fpioa_manager import fm
from Maix import FPIOA, GPIO

BACK = 11
ENTER = 10
NEXT = 16

Match = [[None, (1, 0)], [(2, 1), None]]

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
        # if self.home_button.value() == 0:
        #     sys.exit()

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

        tmp = Match[self.home_button.value()][self.home_last]
        if tmp:
            self.cache['home'], self.home_last = tmp

        tmp = Match[self.back_button.value()][self.back_last]
        if tmp:
            self.cache['back'], self.back_last = tmp

        tmp = Match[self.next_button.value()][self.next_last]
        if tmp:
            self.cache['next'], self.next_last = tmp

PIR = 16

class ttgo_button:

    def __init__(self):
        self.home_last = 1
        self.cache = {
            'home':0,
        }

        fm.register(PIR, fm.fpioa.GPIOHS16)
        self.home_button = GPIO(GPIO.GPIOHS16, GPIO.IN, GPIO.PULL_UP)

    def home(self):
        tmp, self.cache['home'] = self.cache['home'], 0
        return tmp

    def event(self):

        tmp = Match[self.home_button.value()][self.home_last]
        if tmp:
            self.cache['home'], self.home_last = tmp

if __name__ == "__main__":

    #tmp = ttgo_button()
    #while True:
        #tmp.event()
        #time.sleep_ms(200)
        #print(tmp.home())

    tmp = cube_button()
    while True:
        tmp.event()
        time.sleep_ms(200)
        print(tmp.back(), tmp.home(), tmp.next())
        #print(tmp.home_button.value(), tmp.next_button.value(), tmp.back_button.value())
