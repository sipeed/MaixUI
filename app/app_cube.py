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
  from ui_3d_launcher import launcher
  from wdt import protect
  from button import sipeed_button, button_io
except ImportError as e:
  print(e)
  from lib.core import agent, system
  from lib.dialog import draw_dialog_alpha
  from ui.ui_canvas import ui, print_mem_free
  from ui.ui_container import container
  from ui.ui_3d_launcher import launcher
  from driver.wdt import protect
  from driver.button import sipeed_button, button_io

class launcher:

  def load():
    self = __class__
    self.h, self.w = 0, 0
    self.value = 0
    self.ctrl = agent()
    self.ctrl.event(10, self.draw)
    def test_once(self):
      container.latest()
      self.remove(test_once)
    self.ctrl.event(5000, test_once)
    button_io.config(10, 11, 16)

  def free():
    self = __class__
    self.ctrl = None

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  #@ui.warp_template(ui.bg_in_draw)
  #@ui.warp_template(ui.anime_in_draw)
  @ui.warp_template(launcher.draw)
  #@ui.warp_template(taskbar.time_draw)
  #@ui.warp_template(taskbar.mem_draw)
  #@catch # need sipeed_button
  def draw():
    ui.display()

  def event():
    self = __class__
    if self.h < 240:
      self.h += 20
    if self.w < 240:
      self.w += 10
    ui.height, ui.weight = self.h, self.w
    self.ctrl.parallel_cycle()

class loading:

  def load():
    self = __class__
    self.h, self.w = 0, 0
    self.ctrl = agent()
    self.ctrl.event(5, self.draw)
    def into_launcher(self):
      container.reload(launcher)
      self.remove(into_launcher)
    self.ctrl.event(2000, into_launcher)
    #loading.draw()

  def free():
    self = __class__
    self.ctrl = None
    ui.height, ui.weight = 240, 240

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(ui.help_in_draw)
  def draw():
    ui.display()

  def event():
    self = __class__
    if self.h < 240:
      self.h += 10
    if self.w < 240:
      self.w += 10
    ui.height, ui.weight = self.h, self.w
    self.ctrl.parallel_cycle()

if __name__ == "__main__":
  system = agent()
  container.reload(loading)

  last = time.ticks_ms()
  while True:
    while True:
      last = time.ticks_ms() - 1
      while True:
        try:
          #time.sleep(0.1)
          #print(1000 // (time.ticks_ms() - last), 'fps')
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
