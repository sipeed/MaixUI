# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from ui_maix import ui

from button import cube_button

import os, machine, ubinascii

from fs import OS

print(dir(OS))

class ui_explorer:

  btn = cube_button()
  files = OS.listdir('/')
  path = '/'
  index = 0
  layer = ['../']
  limit = 2

  def view_ui_explorer(path='/',selected=0):
    x_offset, y_offset = 10, 25

    ui.img.draw_string(x_offset, y_offset, ui_explorer.path)

    files = OS.listdir('/')

    y_offset += 20

    ui.img.draw_string(x_offset, y_offset, str(files))



  def draw():
    ui_explorer.btn.event()

    if ui_explorer.btn.back() == 1:
        ui_explorer.index -= 1

    elif ui_explorer.btn.next() == 1:
        ui_explorer.index += 1

    x_offset, y_offset = 10, 25

    path = '/'

    ui_explorer.files = OS.listdir(path)

    ui_explorer.files.append(path)

    for i in range(0, ui_explorer.index):
        ui_explorer.files.append(ui_explorer.files.pop(0))

    ui.img.draw_string(x_offset, y_offset, str(ui_explorer.files))

    ui_explorer.index = ui_explorer.index % len(ui_explorer.files)


    #ui_explorer.view_ui_explorer()

    # y_offset += 18
    # for i in range(self.current_offset, len(self.current_dir_files)):
    #     gc.collect()
    #     file_name = self.current_dir_files[i]
    #     # print(file_name)
    #     try:
    #         f_stat = os.stat(self.path + file_name)
    #         if len(file_name) > 16:
    #             file_name = file_name[0:14] + ".."
    #         if S_ISDIR(f_stat[0]):
    #             file_name = file_name + '/'
    #         gc.collect()
    #         file_readable_size = sizeof_fmt(f_stat[6])
    #         img.draw_string(lcd.width() - 50, y_offset,
    #                         file_readable_size, lcd.BLUE)
    #     except Exception as e:
    #         print("-------------------->", e)
    #     is_current = self.current_selected_index == i
    #     line = "%s %d %s" % ("->" if is_current else "  ", i, file_name)
    #     img.draw_string(x_offset, y_offset, line, lcd.RED)
    #     # gc.collect()
    #     y_offset += 18
    #     if y_offset > lcd.height():
    #         print(y_offset, lcd.height(), "y_offset > height(), break")
    #         break


if __name__ == "__main__":

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.bg_in_draw)
    #@ui.warp_template(ui.anime_in_draw)
    @ui.warp_template(ui_explorer.draw)
    def unit_test():
      ui.display()

    import time
    while True:
        unit_test()
