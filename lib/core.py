
# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

class agent:

  def __init__(self):
    self.msg = []
    self.arg = {}

  def get_ms(self):
    import time
    # return time.time() * 1000
    return time.ticks_ms()

  def event(self, interval, function):
    # arrived, interval, function
    tmp = (self.get_ms() + interval, interval, function)
    #print('self.event', tmp)
    self.msg.append(tmp)

  def remove(self, func):
    #print(self.remove)
    for pos in range(len(self.msg)): # maybe use map
      #print(self.msg[pos][2], func)
      if self.msg[pos][2] == func:
          self.msg.remove(self.msg[pos])
          break
    #print(self.msg)

  def cycle(self):
    if (len(self.msg)):
      tmp = self.msg[0]
      if (self.get_ms() >= tmp[0]):
        self.msg.pop(0)
        self.event(tmp[1], tmp[2])
        tmp[2](self)  # function

  def parallel_cycle(self):
    for pos in range(len(self.msg)): # maybe use map
      tmp = self.msg[pos]
      if (self.get_ms() >= tmp[0]):
        #print('self.parallel_cycle', pos, tmp)
        self.msg.pop(pos)
        self.event(tmp[1], tmp[2])
        tmp[2](self)  # function
        break

  def unit_test(self):

    class tmp:
        def test_0(self):
          print('test_0')

        def test_1(self):
          print('test_1')

        def test_2(self):
          print('test_2')
          self.remove(tmp.test_1)
          self.event(1000, tmp.test_1)
          self.remove(tmp.test_2)

    import time
    self.event(200, tmp.test_0)
    self.event(10, tmp.test_1)
    self.event(2000, tmp.test_2)
    while True:
      self.parallel_cycle()
      time.sleep(0.1)

system = agent()

if __name__ == "__main__":
  #agent().unit_test()
  system.unit_test()
