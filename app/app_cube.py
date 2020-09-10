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
except ImportError as e:
  print(e)
  from lib.core import agent, system
  from lib.dialog import draw_dialog_alpha
  from ui.ui_canvas import ui, print_mem_free
  from ui.ui_container import container
  from driver.wdt import protect

class loading:

  def into_launcher(ctrl):
    container.reload(launcher)
    ctrl.remove(loading.into_launcher)

  def load():
    loading.h, loading.w = 0, 0
    loading.ctrl = agent()
    loading.ctrl.event(5, loading.draw)
    loading.ctrl.event(2000, loading.into_launcher)
    #loading.draw()

  def free():
    loading.ctrl = None
    ui.height, ui.weight = 240, 240

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(ui.help_in_draw)
  def draw():
    ui.display()

  def event():
    if loading.h < 240:
      loading.h += 5
    if loading.w < 240:
      loading.w += 5
    ui.height, ui.weight = loading.h, loading.w
    loading.ctrl.parallel_cycle()

class launcher:

  ctrl, value = None, None

  def load():
    launcher.value = 0
    launcher.ctrl = agent()
    launcher.ctrl.event(10, launcher.draw)

  def free():
    launcher.ctrl = None

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(ui.anime_in_draw)
  #@ui.warp_template(taskbar.time_draw)
  #@ui.warp_template(taskbar.mem_draw)
  #@catch # need sipeed_button
  def draw():
    ui.display()

  def event():
    launcher.ctrl.cycle()

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
          print(1000 // (time.ticks_ms() - last), 'fps')
          last = time.ticks_ms()

          gc.collect()
          container.forever()
          system.parallel_cycle()

          protect.keep()
          #gc.collect()
          print_mem_free()
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
