# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from machine import I2C
import math
import os
import image

try:
    from ui_canvas import ui
    from touch import Touch, TouchLow
    from button import sipeed_button, button_io
    from core import agent
except ImportError:
    from ui.ui_canvas import ui
    from driver.touch import Touch, TouchLow
    from driver.button import sipeed_button, button_io
    from lib.core import agent


class icon:

  def __init__(self, x, y, w=64, h=64):
    self.x, self.y, self.w, self.h = x, y, w, h
    self.img = image.Image(size=(self.w, self.h))

  def checked(self, color=(255, 0, 0)):
    ui.canvas.draw_rectangle(self.x - 2, self.y - 2,
                             self.w + 4, self.h + 4, color, thickness=1)

  def on_draw(self):
    tmp = b"\x1F\x3F\x78\xF0\xE3\xC7\xCC\xCC\xCF\xCF\xC7\xE3\xF0\x78\x3F\x1F\xF8\xFC\x1E\x0F\xC7\xE3\xF3\xF3\xF3\xB3\xE3\xC7\x0F\x1E\xFC\xF8"

    self.img.draw_font(0, 0, 16, 16, tmp, scale=4, color=(64, 64, 64))
    self.img.draw_font(0, 0, 16, 16, tmp, scale=4, color=(255, 255, 255))

  def on_title(self, color=(255, 255, 255)):
    ui.canvas.draw_string(self.x, self.y + self.h + 5,
                          self.__qualname__, scale=2)

  def draw(self, is_check=False, alpha=0, color=(255, 255, 255)):
    self.img.clear()

    self.on_draw()

    #ui.canvas.draw_string(self.x, self.y, str(alpha))
    if is_check:
      self.checked(color)

    old = (self.img.width(), self.img.height())
    new = (int(alpha / 50), int(alpha / 50))
    tmp = self.img.resize(old[0] + new[0] - 10, old[1] + new[1] - 10)
    ui.canvas.draw_image(tmp,
        self.x - int(new[0] / 2) + 5,
        self.y - int(new[1] / 2) + 5,
        alpha=int(alpha))  # 4ms
    del tmp

    self.on_title()


class Camera(icon):

    tmp1 = b"\x00\x3E\x22\x7F\xFF\xC0\xC7\xCF\xDC\xD8\xDC\xCF\xC7\xC0\xFF\x7F\x00\x00\x00\xFE\xFF\x03\x9B\xC3\xE3\x63\xE3\xC3\x83\x03\xFF\xFE"
    tmp2 = b"\x00\x00\x00\x00\x00\x00\x07\x0F\x1C\x18\x1C\x0F\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\xC0\xE0\x60\xE0\xC0\x80\x00\x00\x00"

    def on_draw(self):

        #self.img.draw_font(1, 1, 16, 16, Camera.tmp1,
                           #scale=4, color=(64, 64, 64))
        self.img.draw_font(0, 0, 16, 16, Camera.tmp1,
                           scale=4, color=(255, 255, 255))
        self.img.draw_font(0, 0, 16, 16, Camera.tmp2,
                           scale=4, color=(93, 116, 93))

    def on_title(self, color=(105, 105, 105)):
        ui.canvas.draw_string(self.x - 3, self.y + self.h + 5,
                              self.__qualname__, scale=2, color=color)


class System(icon):

    tmp1 = b"\x00\x03\x19\x3B\x3F\x0E\x5C\x78\x78\x5C\x0E\x3F\x3B\x19\x03\x00\x00\xC0\x98\xDC\xFC\x70\x3A\x1E\x1E\x3A\x70\xFC\xDC\x98\xC0\x00"
    tmp2 = b"\x00\x00\x00\x03\x0F\x0E\x1C\x18\x18\x1C\x0E\x0F\x03\x00\x00\x00\x00\x00\x00\xC0\xF0\x70\x38\x18\x18\x38\x70\xF0\xC0\x00\x00\x00"

    def on_draw(self):

        self.img.draw_font(2, 2, 16, 16, System.tmp1,
                           scale=4, color=(64, 64, 64))
        self.img.draw_font(0, 0, 16, 16, System.tmp1,
                           scale=4, color=(193, 205, 193))
        self.img.draw_font(0, 0, 16, 16, System.tmp2,
                           scale=4, color=(255, 255, 255))

    def on_title(self, color=(105, 105, 105)):
        ui.canvas.draw_string(self.x, self.y + self.h + 5,
                              self.__qualname__, scale=2, color=color)


class Demo(icon):

    tmp1 = b"\x00\x7F\x40\x40\x7F\x40\x40\x48\x50\x61\x53\x4A\x40\x40\x7F\x00\x00\xFE\x02\x02\xFE\x02\x02\x52\xCA\x86\x0A\x12\x02\x02\xFE\x00"
    tmp2 = b"\x00\x7F\x40\x40\x7F\x40\x40\x40\x40\x40\x40\x40\x40\x40\x7F\x00\x00\xFE\x02\x02\xFE\x02\x02\x02\x02\x02\x02\x02\x02\x02\xFE\x00"

    def on_draw(self):

        self.img.draw_font(1, 1, 16, 16, Demo.tmp1,
                           scale=4, color=(64, 64, 64))
        self.img.draw_font(0, 0, 16, 16, Demo.tmp1, scale=4,
                           color=(84, 255, 159))
        self.img.draw_font(0, 0, 16, 16, Demo.tmp2, scale=4,
                           color=(47, 79, 79))

    def on_title(self, color=(105, 105, 105)):
        ui.canvas.draw_string(self.x + 10, self.y + self.h + 5,
                              self.__qualname__, scale=2, color=color)


class Photo(icon):

    tmp1 = b"\x3F\x60\xC0\x80\x80\x80\x80\x90\xB8\xEC\xC6\x83\x81\xC0\x60\x3F\xFC\x06\x3B\x6D\x45\x6D\x39\x01\x01\x41\xE1\xB1\x19\x0F\x06\xFC"
    tmp2 = b"\x00\x00\x00\x00\x00\x00\x00\x10\x38\x6C\x46\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\xE0\xB0\x18\x0E\x00\x00"
    tmp3 = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x38\x6C\x44\x6C\x38\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def on_draw(self):

        self.img.draw_font(1, 1, 16, 16, Photo.tmp1,
                           scale=4, color=(64, 64, 64))
        self.img.draw_font(0, 0, 16, 16, Photo.tmp1,
                           scale=4, color=(255, 165, 0))
        self.img.draw_font(0, 0, 16, 16, Photo.tmp2,
                           scale=4, color=(0x0a, 0xa8, 0x58))
        self.img.draw_font(0, 0, 16, 16, Photo.tmp3,
                           scale=4, color=(230, 69, 0))

    def on_title(self, color=(105, 105, 105)):
        ui.canvas.draw_string(self.x + 3, self.y + self.h + 5,
                              self.__qualname__, scale=2, color=color)


class launcher:

  effect = []
  alpha = 0
  app_select = 0
  app_run = False
  app_sets = [
      Camera(60, 200),
      System(160, 200),
      Demo(260, 200),
      Photo(360, 200),
  ]

  toth = Touch(480, 320, 50)
  btn = sipeed_button()
  agent = agent()

  def init():
    launcher.agent.event(150, launcher.key_event)
    launcher.agent.event(50, launcher.touch_event)

  def touch_event(args):
    launcher.toth.event()
    #print(launcher.toth.state, launcher.toth.points)
    if launcher.toth.state == 1:
      old = launcher.toth.points[0]
      sel = launcher.toth.points[1]
      #if len(launcher.effect) > 8:
        #launcher.effect.pop(0)
      #launcher.effect.append((old[0], old[1]))
      if 250 < sel[2] - old[2] and sel[2] - old[2] < 500:
        launcher.toth.state = 2
    if launcher.toth.state == 2:
      #print(launcher.toth.state, launcher.toth.points)
      #launcher.effect = []
      old = launcher.toth.points[0]
      sel = launcher.toth.points[1]
      #print(sel, old, sel[2] - old[2])
      if sel[2] - old[2] < 1000:
        # start
        #if 136 < sel[1] and sel[1] < 200:
        for i in range(len(launcher.app_sets)):
          p = launcher.app_sets[i]
          x, y = p.x, 320 - p.y
          # print(x, p.w, y, p.h)
          if x < sel[0] and sel[1] < y and sel[0] < x + p.w and y - p.h < sel[1]:
            launcher.app_select = i
            if sel[2] - old[2] < 250:
              print('launcher.app_select', launcher.app_select)
              launcher.app_run = True

  def key_event(args):
    launcher.btn.event()

    if launcher.btn.back() == 1:
        launcher.app_select -= 1
    elif launcher.btn.next() == 1:
        launcher.app_select += 1
    elif launcher.btn.home() == 1:
        print('start', launcher.app_select)
        # launcher.app_run = True
        # ui.canvas.draw_string(15, 120, '(%s)' % launcher.app_sets[launcher.app_select])

    launcher.app_select = launcher.app_select % len(launcher.app_sets)  # lock pos

  a = b'\x00\x00\x03\x03\x07\x07\x0E\x0E\x1C\x1F\x38\x38\x70\xF0\x00\x00\x00\x00\xC0\xC0\xE0\xE0\x70\x70\x38\xF8\x1C\x1C\x0E\x0F\x00\x00'
  m = b'\x00\x00\x00\x00\x00\x67\x7F\x61\x61\x61\x61\x61\x61\x61\x00\x00\x00\x00\x00\x00\x00\x1C\xFE\x86\x86\x86\x86\x86\x86\x86\x00\x00'
  i = b'\x00\x00\x01\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x80\x00\x00\x80\x80\x80\x80\x80\x80\x80\x80\x80\x00\x00'
  g = b'\x00\x00\x00\x00\x00\x07\x1C\x18\x38\x1C\x1F\x30\x1F\x30\x70\x1F\x00\x00\x00\x00\x00\xCE\x72\x30\x38\x70\xC0\x00\xF8\x0C\x0E\xF8'
  o = b'\x00\x00\x00\x00\x00\x03\x1E\x38\x70\x70\x70\x38\x1C\x03\x00\x00\x00\x00\x00\x00\x00\xC0\x78\x1C\x0C\x0E\x0E\x1C\x38\xC0\x00\x00'

  def draw():
    launcher.agent.parallel_cycle()

    #ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight),
                                      #fill = True, color = (0, 0, 0))
    #ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight), fill = True, color = (0x70, 0x80, 0x90))
    ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight), fill = True, color = (215, 228, 181))
    #ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight),
                                      #fill = True, color = (37, 40, 55))
    #ui.canvas.draw_string(203, 73, "Amigo",
                          #color=(64, 64, 64), scale=8, mono_space=0)
    ui.canvas.draw_font(182, 82, 16, 16, launcher.a, scale=5, color=(37, 40, 55))
    ui.canvas.draw_font(180, 80, 16, 16, launcher.a, scale=5, color=(0x2d, 0x85, 0xf0))
    ui.canvas.draw_font(252, 82, 16, 16, launcher.m, scale=4, color=(37, 40, 55))
    ui.canvas.draw_font(250, 80, 16, 16, launcher.m, scale=4, color=(0xf4, 0x43, 0x3c))
    ui.canvas.draw_font(292, 82, 16, 16, launcher.i, scale=4, color=(37, 40, 55))
    ui.canvas.draw_font(290, 80, 16, 16, launcher.i, scale=4, color=(0xff, 0xbc, 0x32))
    ui.canvas.draw_font(332, 77, 16, 16, launcher.g, scale=4, color=(37, 40, 55))
    ui.canvas.draw_font(330, 75, 16, 16, launcher.g, scale=4, color=(0x0a, 0xa8, 0x58))
    ui.canvas.draw_font(392, 82, 16, 16, launcher.o, scale=4, color=(37, 40, 55))
    ui.canvas.draw_font(390, 80, 16, 16, launcher.o, scale=4, color=(0xf4, 0x43, 0x3c))
    #ui.canvas.draw_string(200, 70, "A",
                        #color=(0x2d, 0x85, 0xf0), scale=8, mono_space=0)
    #ui.canvas.draw_string(200, 70, "  m",
                        #color=(0xf4, 0x43, 0x3c), scale=8, mono_space=0)
    #ui.canvas.draw_string(200, 70, "    i",
                        #color=(0xff, 0xbc, 0x32), scale=8, mono_space=0)
    #ui.canvas.draw_string(200, 70, "     g",
                        #color=(0x0a, 0xa8, 0x58), scale=8, mono_space=0)
    #ui.canvas.draw_string(200, 70, "       o",
                        #color=(0xf4, 0x43, 0x3c), scale=8, mono_space=0)

    value = math.cos(math.pi * launcher.alpha / 12) * 50 + 200
    launcher.alpha = (launcher.alpha + 1) % 24

    for pos in range(0, len(launcher.app_sets)):
        checked = (pos == launcher.app_select)
        launcher.app_sets[pos].draw(checked, value if checked else 255)

    #for pos in range(len(launcher.effect)):
        #tmp = launcher.effect[pos]
        #cor = (pos + 1) * 32
        #ui.canvas.draw_circle(tmp[0], 320 - tmp[1], (pos + 1) * 3, thickness=1, fill=False, color=(cor, cor, cor))

    launcher.agent.parallel_cycle()

launcher.init()

if __name__ == "__main__":
  from ui_canvas import ui
  ui.height, ui.weight = 480, 320
  button_io.config(23, 31, 20) # amigo
  TouchLow.config(I2C(I2C.I2C3, freq=1000*1000, scl=24, sda=27)) # amigo
  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(launcher.draw)
  @ui.warp_template(ui.bg_in_draw)
  def unit_test():
    ui.display()
  import time
  last = time.ticks_ms()
  while True:
      #print(time.ticks_ms() - last)
      last = time.ticks_ms()
      unit_test()
      #time.sleep(0.5)
