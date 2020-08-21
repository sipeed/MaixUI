# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import math, os, image

try:
    from ui_canvas import ui
    from button import sipeed_button, button_io
    from core import agent
except ImportError:
    from ui.ui_canvas import ui
    from driver.button import sipeed_button, button_io
    from lib.core import agent

class icon:

  def __init__(self, x, y, path):
    self.img = image.Image(path)  # 60ms ~ 90ms
    self.x, self.y = x, y
    self.w, self.h = self.img.width(), self.img.height()
    self.last = 0

  def checked(self, color=(255, 0, 0)):
    ui.canvas.draw_rectangle(self.x - 2, self.y - 2,
                             self.w + 4, self.h + 4, color, thickness=1)

  def draw(self, is_check=False, alpha=0, color=(255, 255, 255)):
    tmp = self.img.copy()  # 1ms
    if is_check:
      self.checked(color)

    old = (tmp.width(), tmp.height())
    new = (int(alpha / 50), int(alpha / 50))
    tmp = tmp.resize(old[0] + new[0] - 3, old[1] + new[1] - 3)
    #print(tmp)
    #if self.last != new[0]:
        ##print(old, new)
        #tmp = tmp.resize(old[0] + new[0] - 8, old[1] + new[1] - 8)
        #self.last = new[0]
    #print(tmp)
    ui.canvas.draw_image(tmp,
        self.x - int(new[0] / 2),
        self.y - int(new[1] / 2),
        alpha=int(alpha))  # 4ms
    del tmp

  def title(self, string, color=(255, 255, 255)):
    ui.canvas.draw_string(self.x, self.y, string)


class launcher:

  alpha = 0
  app_select = 0
  app_sets = [
      icon(60, 200, os.getcwd() + "/res/icons/app_camera.bmp"),
      icon(160, 200, os.getcwd() + "/res/icons/app_settings.bmp"),
      icon(260, 200, os.getcwd() + "/res/icons/app_explorer.bmp"),
      icon(360, 200, os.getcwd() + "/res/icons/app_system_info.bmp"),
  ]

  btn = sipeed_button()
  agent = agent()

  def init():
    launcher.agent.event(150, launcher.key_event)

  def key_event():
    launcher.btn.event()

    if launcher.btn.back() == 1:
        launcher.app_select -= 1
    elif launcher.btn.next() == 1:
        launcher.app_select += 1
    elif launcher.btn.home() == 1:
        print('start', launcher.app_select)
        # ui.canvas.draw_string(15, 120, '(%s)' % launcher.app_sets[launcher.app_select])

    launcher.app_select = launcher.app_select % len(launcher.app_sets)  # lock pos


  def draw():
    launcher.agent.parallel_cycle()
    ui.canvas.draw_string(203, 73, "Amigo",
                          color=(64, 64, 64), scale=8, mono_space=0)
    ui.canvas.draw_string(200, 70, "A",
                        color=(0xFF, 0x30, 0x30), scale=8, mono_space=0)
    ui.canvas.draw_string(200, 70, "  m",
                        color=(0xFF, 0xFF, 0x30), scale=8, mono_space=0)
    ui.canvas.draw_string(200, 70, "    i",
                        color=(0x30, 0x30, 0xFF), scale=8, mono_space=0)
    ui.canvas.draw_string(200, 70, "     g",
                        color=(0x30, 0xFF, 0x30), scale=8, mono_space=0)
    ui.canvas.draw_string(200, 70, "       o",
                        color=(0xFF, 0x30, 0xFF), scale=8, mono_space=0)

    value = math.cos(math.pi * launcher.alpha / 12) * 50 + 200
    launcher.alpha = (launcher.alpha + 1) % 24

    for pos in range(0, len(launcher.app_sets)):
        checked = (pos == launcher.app_select)
        launcher.app_sets[pos].draw(checked, value if checked else 255)

launcher.init()

if __name__ == "__main__":
  from ui_canvas import ui
  ui.height, ui.weight = 480, 320
  button_io.config(23, 31, 20) # amigo
  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(launcher.draw)
  def unit_test():
    ui.display()
  import time
  last = time.ticks_ms()
  while True:
      print(time.ticks_ms() - last)
      last = time.ticks_ms()
      unit_test()
      #time.sleep(0.5)
