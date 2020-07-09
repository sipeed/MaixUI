# This file is part of MaixUI
# Copyright (c) 2020 sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

#!/usr/bin/env python
# coding: utf-8

# In[53]:


import sys, time


Match = [[None, (1, 0)], [(2, 1), None]]
Match1 = [[None, 1], [2, None]]
Match2 = [[None, 0], [1, None]]

class GPIO:
    GPIOHS11 = None
    GPIOHS16 = None
    IN = None
    PULL_UP = None

    def __init__(self, *_):
        self.t = 1

    def value(self):
        self.t = 1 - self.t
        return self.t


class cube_button:
    def __init__(self):
        self.home_last, self.next_last, self.back_last = 1, 1, 1
        self.cache = {
            'home':0,
            'next':0,
            'back':0,
        }
        self.home_button = GPIO(GPIO.GPIOHS11, GPIO.IN, GPIO.PULL_UP)
        self.back_button = GPIO(GPIO.GPIOHS11, GPIO.IN, GPIO.PULL_UP)
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

    def event2(self):
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

    def event3(self):
        tmp1 = Match1[self.home_button.value()][self.home_last]
        tmp2 = Match2[self.home_button.value()][self.home_last]

        if tmp1 and tmp2:
            self.cache['home'] = tmp1
            self.home_last = tmp2


        tmp1 = Match1[self.home_button.value()][self.home_last]
        tmp2 = Match2[self.home_button.value()][self.home_last]

        if tmp1 and tmp2:
            self.cache['back'] = tmp1
            self.back_last = tmp2


        tmp1 = Match1[self.home_button.value()][self.home_last]
        tmp2 = Match2[self.home_button.value()][self.home_last]

        if tmp1 and tmp2:
            self.cache['next'] = tmp1
            self.next_last = tmp2



if __name__ == "__main__":

    tmp = cube_button()
    n = 10000

    t = time.ticks()
    for i in range(n):
        tmp.event()
    print(time.ticks() - t)

    t = time.ticks()
    for i in range(n):
        tmp.event2()
    print(time.ticks() - t)

    t = time.ticks()
    for i in range(n):
        tmp.event3()
    print(time.ticks() - t)


