# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math

try:
  from core import agent, system
  from dialog import draw_dialog_alpha
  from ui_canvas import ui, print_mem_free
  from ui_container import container
  from wdt import protect
  from creater import get_time_curve, get_count_curve
except ImportError as e:
  print(e)
  from lib.core import agent, system
  from lib.dialog import draw_dialog_alpha
  from ui.ui_canvas import ui, print_mem_free
  from ui.ui_container import container
  from driver.wdt import protect
  from lib.creater import get_time_curve, get_count_curve

class message:

  def load():
    __class__.state = 0
    __class__.count = 0
    __class__.ctrl = agent()
    __class__.ctrl.event(20, __class__.draw)
    def test_once(self):
        self.remove(test_once)
        if __class__.state == 1:
            __class__.state = 2
    __class__.ctrl.event(3000, test_once)

  def free():
    __class__.ctrl = None

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  @ui.warp_template(ui.bg_in_draw)
  def draw():
      l, r, w, h = 60, 60, 120, 120
      if __class__.state == 0:
          __class__.count += 1
          value = abs(int(get_count_curve(__class__.count, 3, 50) * 10))
          #print(value)

          pos = draw_dialog_alpha(ui.canvas, l - value // 2, r - value // 2, w + value, h + value, 10, color=(255, 0, 0), alpha=230)
          if value >= 9:
              __class__.state = 1

      if __class__.state == 1:

          pos = draw_dialog_alpha(ui.canvas, l, r, w, h, 10, color=(255, 0, 0), alpha=230)
          text = "It will show Message , return last pages after 3s"

          chunks, chunk_size = len(text), w // 12
          msg_lines = [text[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
          for i in range(len(msg_lines)):
              ui.canvas.draw_string(pos[0] + 16, pos[1] + 8 + 26 * i, msg_lines[i], scale=2, color=(0, 0, 0))

      if __class__.state == 2:
          __class__.count += 1
          value = abs(int(get_count_curve(__class__.count, 3, 50) * 10))

          pos = draw_dialog_alpha(ui.canvas, l - value // 2, r - value // 2, w + value, h + value, 10, color=(255, 0, 0), alpha=230)
          if value == 0:
              container.latest()

      ui.display()
  def event():
    __class__.ctrl.parallel_cycle()

class slide_list:

  def load():
    __class__.state = 0
    __class__.lists = ['123', '456', '789', 'abc', 'efg']
    __class__.selected = 0
    __class__.limit = 100
    __class__.count = 0
    __class__.ctrl = agent()
    __class__.ctrl.event(20, __class__.draw)
    def test_once(self):
        #self.remove(test_once)
        if __class__.state == 0:
            __class__.state = 1
        if __class__.state == 2:
            __class__.state = 3
            #__class__.selected = (__class__.selected + 1) % len(__class__.lists)

    __class__.ctrl.event(2000, test_once)

  def free():
    __class__.ctrl = None

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  @ui.warp_template(ui.bg_in_draw)
  def draw():
      l, r, w, h = 20, 185, 200, 55
      if __class__.state == 1:
          __class__.count += 1
          value = abs(int(get_count_curve(__class__.count + 25, 3, 50) * __class__.limit))
          #print(value)

          pos = draw_dialog_alpha(ui.canvas, l, r + value // 2, w, h, 10, color=(255, 0, 0), alpha=200 - value)
          if value == 0:
              __class__.state = 2

      if __class__.state == 2:

          pos = draw_dialog_alpha(ui.canvas, l, r, w, h, 10, color=(255, 0, 0), alpha=250)
          text = "It will show Message"

          chunks, chunk_size = len(text), w // 11
          msg_lines = [text[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
          for i in range(len(msg_lines)):
              ui.canvas.draw_string(pos[0] + 16, pos[1] + 8 + 26 * i, msg_lines[i], scale=2, color=(0, 0, 0))

      if __class__.state == 3:
          __class__.count += 1
          value = abs(int(get_count_curve(__class__.count + 25, 3, 50) * __class__.limit))
          #print(value)

          pos = draw_dialog_alpha(ui.canvas, l, r + value // 2, w, h, 10, color=(255, 0, 0), alpha=200 - value)
          if value >= __class__.limit - 5:
              #container.latest()
              __class__.count = 0
              __class__.state = 0

      ui.display()
  def event():
    __class__.ctrl.parallel_cycle()

class launcher:

  def load():
    self = __class__
    self.ctrl = agent()
    self.ctrl.event(10, self.draw)
    def show_message(self):
      container.reload(slide_list)
      self.remove(show_message)
    self.ctrl.event(2000, show_message)

  def free():
    self = __class__
    self.ctrl = None

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  @ui.warp_template(ui.bg_in_draw)
  #@ui.warp_template(ui.anime_in_draw)
  #@ui.warp_template(taskbar.time_draw)
  #@ui.warp_template(taskbar.mem_draw)
  #@catch # need sipeed_button
  def draw():
    ui.display()

  def event():
    self = __class__
    self.ctrl.parallel_cycle()

if __name__ == "__main__":

  system = agent()
  container.reload(slide_list)

  while True:
    while True:
      last = time.ticks_ms() - 1
      while True:
        try:
          #time.sleep(0.1)
          print(1000 // (time.ticks_ms() - last), 'fps')
          last = time.ticks_ms()

          gc.collect()
          container.forever()
          system.parallel_cycle()

          protect.keep()
          #gc.collect()
          #print_mem_free()
        except KeyboardInterrupt:
          protect.stop()
          raise KeyboardInterrupt
        #except Exception as e:
          #gc.collect()
          #print(e)
        finally:
          try:
            ui.display()
          except:
            pass
