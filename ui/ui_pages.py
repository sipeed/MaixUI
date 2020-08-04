# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

try:
    from ui_canvas import ui
    from button import cube_button
except ImportError:
    from ui.ui_canvas import ui
    from driver.button import cube_button

import os
import machine
import ubinascii


class sys_info:

  def sizeof_fmt(num, suffix='B'):
      for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
          if abs(num) < 1024.0:
              return "%3.1f%s%s" % (num, unit, suffix)
          num /= 1024.0
      return "%.1f%s%s" % (num, 'Yi', suffix)

  def __init__(self):
      self.__initialized = False

  def __lazy_init(self):
      self.system_uname = os.uname()
      self.device_id = ubinascii.hexlify(machine.unique_id()).decode()
      root_files = os.listdir('/')
      self.fs_info_list = []
      for f in root_files:
          fs_path = '/' + f
          fs_stat = os.statvfs(fs_path)
          bs1 = fs_stat[0]
          bs2 = fs_stat[1]
          total_blocks = fs_stat[2]
          free_blocks = fs_stat[3]
          info = "%s total=%s free=%s" % (
              fs_path,
              sys_info.sizeof_fmt(bs1 * total_blocks),
              sys_info.sizeof_fmt(bs2 * free_blocks)
          )
          self.fs_info_list.append(info)
          print(info)
      self.__initialized = True

  def draw(self, img):
      if not self.__initialized:
          self.__lazy_init()
      img.draw_rectangle(
          (20, 30, 200, 200), fill=True, color=(50, 50, 50))
      x, y = 30, 32
      img.draw_string(x, y, "Information", (255, 0, 0), scale=2)
      y += 22
      img.draw_string(x, y, "-----------------------------", (255, 255, 255))
      y += 16
      img.draw_string(x, y, "Uname:", (255, 0, 0))
      y += 16
      img.draw_string(x, y, self.system_uname.machine, (0, 255, 0))
      y += 20
      #img.draw_string(x, y, "-----------------------------", (255, 255, 255))
      # y += 16
      img.draw_string(x, y, "FirmwareVersion:", (255, 0, 0))
      y += 16
      img.draw_string(x, y, self.system_uname.version[:34], (0, 255, 0))
      y += 20
      #img.draw_string(x, y, "-----------------------------", (255, 255, 255))
      # y += 16
      img.draw_string(x, y, "machine id:", (255, 0, 0))
      y += 16
      img.draw_string(x, y, self.device_id[:30], (0, 255, 0))
      y += 20
      img.draw_string(x, y, "-----------------------------", (255, 255, 255))
      for info in self.fs_info_list:
          y += 16
          img.draw_string(x, y, info, (255, 0, 0))


class pages:

  def __init__(self):
    self.btn = cube_button()
    self.page_info = sys_info()
    self.page = 0

  def draw(self):
    self.btn.event()

    if self.btn.back() == 2:
        self.page -= 1
    elif self.btn.next() == 2:
        self.page += 1
    self.page = self.page % 3

    if self.page == 0:
      ui.canvas.draw_string(20, 30, "Weclome to MaixCube",
                            (255, 124, 12), scale=2)
    if self.page == 1:
      self.page_info.draw(ui.canvas)
    if self.page == 2:
      ui.canvas.draw_string(40, 200, "Enjoy it! :D", (51, 169, 212), scale=2)


if __name__ == "__main__":

    tmp = pages()

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.grey_draw)
    #@ui.warp_template(ui.bg_in_draw)
    @ui.warp_template(ui.anime_draw)
    @ui.warp_template(tmp.draw)
    def unit_test():
      print('1 display : ' + str(gc.mem_free() / 1024) + ' kb')
      ui.display()
      print('2 display : ' + str(gc.mem_free() / 1024) + ' kb')

    import time
    while True:
        print('while True : ' + str(gc.mem_free() / 1024) + ' kb')
        unit_test()
