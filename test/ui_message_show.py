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

class slide_view:

  def load():
    __class__.state = 0
    __class__.limit = 100
    __class__.count = 0
    __class__.ctrl = agent()
    __class__.ctrl.event(20, __class__.draw)
    def test_once(self):
        self.remove(test_once)
        if __class__.state == 0:
            __class__.state = 1
    __class__.ctrl.event(1000, test_once)
    def test_task(self):
        if __class__.state == 0:
            __class__.state = 1
        if __class__.state == 2:
            __class__.state = 3
    __class__.ctrl.event(3000, test_task)


  def free():
    __class__.ctrl = None

  def get_curve():
      __class__.count += 1
      return abs(int(get_count_curve(__class__.count + 25, 3, 50) * __class__.limit))

  def show_slide():
      l, r, w, h = 20, 210, 200, 40
      if __class__.state == 1:
          value = __class__.get_curve()
          pos = draw_dialog_alpha(ui.canvas, l, r + value // 2, w, h, 10, color=(255, 0, 0), alpha=200 - value)
          pos = draw_dialog_alpha(ui.canvas, l + 50, r - 220 - value // 2, w - 100, h, 10, color=(0, 0, 255), alpha=200 - value)
          if value <= 5:
              __class__.state = 2

      if __class__.state == 2:
          text = "It will show Message"
          pos = draw_dialog_alpha(ui.canvas, l, r, w, h, 10, color=(255, 0, 0), alpha=220)
          ui.canvas.draw_string(pos[0] + 8, pos[1] + 10, text, scale=2, color=(0, 0, 0))
          text = "   Camera"
          pos = draw_dialog_alpha(ui.canvas, l + 50, r - 220, w - 100, h, 10, color=(0, 0, 255), alpha=220)
          ui.canvas.draw_string(pos[0] + 8, pos[1] + 25, text, scale=2, color=(0, 0, 0))

      if __class__.state == 3:
          value = __class__.get_curve()
          pos = draw_dialog_alpha(ui.canvas, l, r + value // 2, w, h, 10, color=(255, 0, 0), alpha=200 - value)
          pos = draw_dialog_alpha(ui.canvas, l + 50, r - 220 - value // 2, w - 100, h, 10, color=(0, 0, 255), alpha=200 - value)
          if value >= __class__.limit - 5:
              __class__.state = __class__.count = 0
              #container.latest()

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(ui.anime_in_draw)
  def draw():
      __class__.show_slide()

      ui.display()
  def event():
    __class__.ctrl.parallel_cycle()

class shift_view:

  def load():
    __class__.state = 0
    __class__.lists = ['', '456789', '789abc', 'abcefg', '']
    __class__.selected = 0
    __class__.limit = 90
    __class__.count = 0
    __class__.ctrl = agent()
    __class__.ctrl.event(20, __class__.draw)
    #def test_once(self):
        #self.remove(test_once)
        #if __class__.state == 0:
            #__class__.state = 1
    #__class__.ctrl.event(1000, test_once)
    def test_task(self):
        __class__.count = 0
        if time.ticks_ms() % 2:
            __class__.state = 1
        else:
            __class__.state = 3
    __class__.ctrl.event(1000, test_task)

  def free():
    __class__.ctrl = None

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(ui.anime_in_draw)
  def draw():
    x, y, w, h = -80, 210, 400, 40

    v = 0

    if __class__.state == 1:
        __class__.count += 1
        v = (int(get_count_curve(__class__.count, 2, 120) * __class__.limit))
        if v > __class__.limit // 2:
            __class__.state = 2

    if __class__.state == 3:
        __class__.count -= 1
        v = -(int(get_count_curve(__class__.count, 2, 120) * __class__.limit))
        if v < -__class__.limit // 2:
            __class__.state = 4

    tmp = image.Image(size=(w, h))
    tmp.draw_rectangle((0, 0, w, h), fill=True, color=(120, 120, 120))
    for i in range(0, w, 80):
        c = (200, 200, 200)
        if i == 160:
            c = (255, 255, 255)
        tmp.draw_string(i + 5, 5, __class__.lists[i // 80], scale=2, color=c)
    ui.canvas.draw_image(tmp, x - v, y, alpha=255)
    del tmp

    if __class__.state == 2:
        if __class__.lists[-2] != '':
            __class__.lists.append(__class__.lists.pop(0))
        __class__.state = 0

    if __class__.state == 4:
        if __class__.lists[1] != '':
            __class__.lists.insert(0, __class__.lists.pop(-1))
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
      container.reload(slide_view)
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
  container.reload(shift_view)

  while True:
    while True:
      last = time.ticks_ms() - 1
      while True:
        print(1000 // (time.ticks_ms() - last), 'fps')
        last = time.ticks_ms()
        try:
          gc.collect()
          container.forever()
          system.parallel_cycle()
          protect.keep()
          #gc.collect()
          #print_mem_free()
          #time.sleep(0.05)
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
