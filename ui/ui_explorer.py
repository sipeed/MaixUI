# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#


try:
    from ui_maix import ui
    from button import cube_button
    from fs import OS
except ImportError:
    from ui.ui_maix import ui
    from driver.button import cube_button
    from driver.fs import OS

import os
import machine
import ubinascii


def list_rshift(obj):
    obj.insert(0, obj[-1])
    obj.pop(-1)
    return obj

#print(list_rshift([0, 1, 2]))


def list_lshift(obj):
    obj.append(obj.pop(0))
    return obj

#print(list_lshift([0, 1, 2]))


class explorer:

  btn = cube_button()
  files = OS.listdir('/') + ["/"]
  paths = ["/"]
  info = ""

  def load_explorer(path='/'):
    if '../' == path:  # return
        #print(2, explorer.paths, explorer.files)
        explorer.paths.pop(-1)
        if len(explorer.paths) > 1:
            explorer.files = OS.listdir(explorer.get_path(explorer.paths[-1]))
            explorer.files.insert(0, '../')
        else:
            explorer.files = OS.listdir('/')
            explorer.files.insert(0, '/')
        #print(3, explorer.paths, explorer.files)
        return  # !

    if explorer.paths[-1] != path:  # >>>
        if path[0] != '/':
          path = '/' + path
        explorer.paths.append(path)
        #print(0, explorer.get_path(explorer.paths), OS.listdir(explorer.get_path(explorer.paths)))
        explorer.files = OS.listdir(explorer.get_path(explorer.paths))
        explorer.files.insert(0, '../')
        #print(1, explorer.paths, explorer.files)
        return  # !

  def get_path(paths=[]):
      tmp_path = ''
      for p in explorer.paths:
          tmp_path += p if p != '/' else ''
      return tmp_path

  def draw():
    explorer.btn.event()

    if explorer.btn.back() == 1:
        list_rshift(explorer.files)
    elif explorer.btn.next() == 1:
        list_lshift(explorer.files)
    elif explorer.btn.home() == 1:
        tmp = explorer.files[0]
        # if tmp == '/':
        #     raise Exception('exit explorer...')
        if tmp in ["../"] or tmp.find('.') == -1:
            explorer.load_explorer(tmp)
            list_lshift(explorer.files)
        else:
            explorer.info = tmp

    ui.canvas.draw_rectangle((0, 0, 240, 240), fill=True, color=(50, 50, 50))

    ui.canvas.draw_string(10, 5, str(
        explorer.get_path(explorer.paths)), scale=1)

    ui.canvas.draw_string(10, 225, str(explorer.info), scale=1)

    list_size = len(explorer.files)

    if list_size > 4:
        tmp = (150, 150, 150)
        ui.canvas.draw_rectangle(
            (65, 25, 200, 25), fill=True, color=(75, 75, 75))
        ui.canvas.draw_string(70, 30, str(
            explorer.files[-2]), scale=1, color=tmp)
        ui.canvas.draw_rectangle(
            (65, 195, 200, 25), fill=True, color=(75, 75, 75))
        ui.canvas.draw_string(70, 200, str(
            explorer.files[+2]), scale=1, color=tmp)

    if list_size > 2:
        tmp = (200, 200, 200)
        ui.canvas.draw_rectangle(
            (45, 55, 200, 35), fill=True, color=(100, 100, 100))
        ui.canvas.draw_string(50, 60, str(
            explorer.files[-1]), scale=2, color=tmp)
        ui.canvas.draw_rectangle(
            (45, 155, 200, 35), fill=True, color=(100, 100, 100))
        ui.canvas.draw_string(50, 160, str(
            explorer.files[+1]), scale=2, color=tmp)

    if list_size > 0:
        tmp = (255, 255, 255)
        #ui.canvas.draw_ellipse(120, 120, 200, 25, 0, color=(226, 205, 223), thickness=2, fill=True)
        ui.canvas.draw_rectangle(
            (20, 95, 220, 55), fill=True, color=(0x5b, 0x86, 0xec))
        ui.canvas.draw_string(30, 105, str(
            explorer.files[0]), scale=3, color=tmp)


if __name__ == "__main__":

    @ui.warp_template(ui.blank_draw)
    #@ui.warp_template(ui.bg_in_draw)
    #@ui.warp_template(ui.anime_in_draw)
    @ui.warp_template(explorer.draw)
    def unit_test():
      ui.display()

    import time
    while True:
        unit_test()
