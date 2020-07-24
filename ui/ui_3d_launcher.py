# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import math, os, image

try:
    from ui_maix import ui
    from button import cube_button
    from core import agent
except ImportError:
    from ui.ui_maix import ui
    from driver.button import cube_button
    from lib.core import agent

class icon:

  x, y, w, h, img = 0, 0, 0, 0, None

  def __init__(self, x, y, path):
    self.img = image.Image(path)  # 60ms ~ 90ms
    self.x, self.y = x, y
    self.w, self.h = self.img.width(), self.img.height()

  def checked(self, color=(255, 0, 0), x = None, y = None):
    ui.canvas.draw_rectangle(x - 2, y - 2,
                             self.w + 4, self.h + 4, color, thickness=1)

  def draw(self, is_check=False, alpha=0, color=(255, 255, 255), x = None, y = None, scale = 1.0):
    tmp = self.img.copy()  # 1ms
    if x == None:
        x = self.x
    if y == None:
        y = self.y
    if is_check:
      self.checked(color, x=x, y=y)

    tmp = tmp.resize(int(tmp.width() * scale), int(tmp.height() * scale))

    ui.canvas.draw_image(tmp, x, y, alpha=int(alpha))  # 4ms
    del tmp

  def title(self, string, color=(255, 255, 255)):
    ui.canvas.draw_string(self.x, self.y, string)


class launcher:

  alpha = 0
  app_select = 0
  app_sets = [
      icon(40, 50, os.getcwd() + "/res/icons/app_camera.bmp"),
      icon(140, 50, os.getcwd() + "/res/icons/app_settings.bmp"),
      icon(40, 150, os.getcwd() + "/res/icons/app_explorer.bmp"),
      icon(140, 150, os.getcwd() + "/res/icons/app_system_info.bmp")
  ]

  btn = cube_button()
  agent = agent()

  def init():
    launcher.agent.event(150, launcher.key_event)

  def key_event():
    launcher.btn.event()

    if launcher.btn.back() == 1:
        if launcher.goal == 0:
            launcher.goal = -20
    elif launcher.btn.next() == 1:
        if launcher.goal == 0:
            launcher.goal = +20
    elif launcher.btn.home() == 1:
        print('start', launcher.app_select)
        # ui.canvas.draw_string(15, 120, '(%s)' % launcher.app_sets[launcher.app_select])

    #launcher.goal = launcher.goal % 120 # lock pos

  pos, goal = 0, 0

  def load(app_pos, app_select):
    pos = app_pos * (math.pi / 60)
    tmp = (120 * math.sin(pos), 80 * math.cos(pos + 0.2))

    #ui.canvas.draw_line(120, 100, 120 + int(tmp[0]), 120 + int(tmp[1]), color=(150, 150, 150))

    x, y = (120 + int(tmp[0] - 30)), (120 + int(tmp[1] - 30))
    s = (y / 240) * 1.8
    #if int(y * s - y - 60) > 0:
    launcher.app_sets[app_select].draw(is_check=False, alpha=y+50, x=x-15, y=int(y * s - y + 40), scale=s)

  def draw():
    launcher.agent.cycle()
    #launcher.app_select = (launcher.app_select + 1) % 120

    if launcher.goal == 0:
        pass
    elif launcher.goal > 0:
        launcher.goal -= 1
        launcher.pos += 1
    elif launcher.goal < 0:
        launcher.goal += 1
        launcher.pos -= 1

    launcher.pos = launcher.pos % 120 # lock pos

    ui.canvas.draw_ellipse(120, 160, 80, 30, -15, color=(
                      150 - launcher.goal * 5, 150 - launcher.goal * 5, 150 - launcher.goal * 5), thickness=2, fill=True)
    launcher.load(launcher.pos, 0)
    launcher.load(launcher.pos - 20, 1)
    launcher.load(launcher.pos - 40, 2)
    launcher.load(launcher.pos - 60, 3)
    launcher.load(launcher.pos - 80, 0)
    launcher.load(launcher.pos - 100, 1)

    #value = math.cos(math.pi * launcher.alpha / 12) * 50 + 200
    #launcher.alpha = (launcher.alpha + 1) % 24

    #for pos in range(0, 4):
        #checked = (pos == launcher.app_select)
        #launcher.app_sets[pos].draw(checked, value if checked else 255)

launcher.init()

if __name__ == "__main__":
  from ui_maix import ui
  from ui_taskbar import taskbar

  @ui.warp_template(ui.grey_draw)
  #@ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(taskbar.time_draw)
  @ui.warp_template(launcher.draw)
  def unit_test():
    ui.display()
  import time
  last = time.ticks_ms()
  while True:
      print(time.ticks_ms() - last)
      last = time.ticks_ms()
      unit_test()
      #time.sleep(0.01)
