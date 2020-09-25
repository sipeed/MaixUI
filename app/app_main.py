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
  from creater import get_time_curve
except ImportError as e:
  print(e)
  from lib.core import agent, system
  from lib.dialog import draw_dialog_alpha
  from ui.ui_canvas import ui, print_mem_free
  from ui.ui_container import container
  from driver.wdt import protect
  from lib.creater import get_time_curve

class launcher:

  def load():
    __class__.ctrl = agent()
    __class__.ctrl.event(20, __class__.draw)

  def free():
    __class__.ctrl = None

  @ui.warp_template(ui.blank_draw)
  @ui.warp_template(ui.grey_draw)
  @ui.warp_template(ui.bg_in_draw)
  @ui.warp_template(ui.anime_in_draw)
  @ui.warp_template(ui.help_in_draw)
  #@ui.warp_template(taskbar.time_draw)
  #@ui.warp_template(taskbar.mem_draw)
  #@catch # need sipeed_button
  def draw():
    height = 100 + int(get_time_curve(3, 250) * 60)
    pos = draw_dialog_alpha(ui.canvas, 20, height, 200, 20, 10, color=(255, 0, 0), alpha=200)
    ui.canvas.draw_string(pos[0] + 10, pos[1] + 10, "Welcome to MaixUI", scale=2, color=(0,0,0))
    ui.display()

  def event():
    __class__.ctrl.cycle()

if __name__ == "__main__":
  system = agent()
  container.reload(launcher)

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
