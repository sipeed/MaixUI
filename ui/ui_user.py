
from ui_maix import ui

from button import cube_button

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
      #img.clear()
      y = 30
      img.draw_string(3, y, "Weclome to MaixCube", (255, 0, 0), scale=2)
      y += 20
      img.draw_string(3, y, "-----------------------------", (255, 255, 255))
      y += 16
      img.draw_string(3, y, "Uname:", (255, 0, 0))
      y += 16
      img.draw_string(3, y, self.system_uname.machine, (0, 255, 0))
      y += 20
      #img.draw_string(3, y, "-----------------------------", (255, 255, 255))
      # y += 16
      img.draw_string(3, y, "FirmwareVersion:", (255, 0, 0))
      y += 16
      img.draw_string(3, y, self.system_uname.version, (0, 255, 0))
      y += 20
      #img.draw_string(3, y, "-----------------------------", (255, 255, 255))
      # y += 16
      img.draw_string(3, y, "machine id:", (255, 0, 0))
      y += 16
      img.draw_string(3, y, self.device_id, (0, 255, 0))
      y += 20
      img.draw_string(3, y, "-----------------------------", (255, 255, 255))
      for info in self.fs_info_list:
          y += 16
          img.draw_string(3, y, info, (255, 0, 0))


class user:

  def __init__(self):
    self.btn = cube_button()
    self.page_info = sys_info()
    self.page = 0

  def draw(self):
    self.btn.event()

    if self.btn.back() == 1:
        self.page -= 1
    elif self.btn.next() == 1:
        self.page += 1
    self.page = self.page % 3

    if self.page == 0:
      ui.img.draw_string(40, 120, "MaixCube", (255, 255, 0), scale=2)
    if self.page == 1:
      self.page_info.draw(ui.img)
    if self.page == 2:
      ui.img.draw_string(40, 200, "Test Pages", (0, 0, 255), scale=2)

if __name__ == "__main__":

    tmp = user()

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(tmp.draw)
    def unit_test():
      ui.display()

    import time
    while True:
        unit_test()