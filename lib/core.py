
# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

class agent:

  def __init__(self):
    self.msg = []

  def get_ms(self):
    import time
    # return time.time() * 1000
    return time.ticks_ms()

  def event(self, interval, function):
    # arrived, interval, function
    tmp = (self.get_ms() + interval, interval, function)
    self.msg.append(tmp)

  def cycle(self):
    if (len(self.msg)):
      tmp = self.msg[0]
      if (self.get_ms() >= tmp[0]):
        self.msg.pop(0)
        self.event(tmp[1], tmp[2])
        tmp[2]() # function

  def unit_test(self):

    def test_0():
      print('test_0')
    def test_1():
      print('test_1')
    def test_2():
      print('test_2')

    import time
    self.event(200, test_0)
    self.event(200, test_1)
    self.event(200, test_2)
    while True:
      self.cycle()
      time.sleep(0.1)

if __name__ == "__main__":
  agent().unit_test()
