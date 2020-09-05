# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

try:
    from ui_canvas import ui
    from button import sipeed_button, button_io
    from fs import OS
    from dialog import draw_dialog_alpha
except ImportError:
    from ui.ui_canvas import ui
    from driver.button import sipeed_button, button_io
    from driver.fs import OS
    from lib.dialog import draw_dialog_alpha

import math

def list_rshift(obj):
    obj.insert(0, obj[-1])
    obj.pop(-1)
    return obj

#print(list_rshift([0, 1, 2]))

def list_lshift(obj):
    obj.append(obj.pop(0))
    return obj

#print(list_lshift([0, 1, 2]))

class CubeListBox:

  btn = sipeed_button()
  files = OS.listdir('/') + ["/"]
  paths = ["/"]
  info = ""

  def load_explorer(path='/'):
    if '../' == path:  # return
        #print(2, CubeListBox.paths, CubeListBox.files)
        CubeListBox.paths.pop(-1)
        if len(CubeListBox.paths) > 1:
            CubeListBox.files = OS.listdir(CubeListBox.get_path(CubeListBox.paths[-1]))
            CubeListBox.files.insert(0, '../')
        else:
            CubeListBox.files = OS.listdir('/')
            CubeListBox.files.insert(0, '/')
        #print(3, CubeListBox.paths, CubeListBox.files)
        return  # !

    if CubeListBox.paths[-1] != path:  # >>>
        if path[0] != '/':
          path = '/' + path
        CubeListBox.paths.append(path)
        #print(0, CubeListBox.get_path(CubeListBox.paths), OS.listdir(CubeListBox.get_path(CubeListBox.paths)))
        CubeListBox.files = OS.listdir(CubeListBox.get_path(CubeListBox.paths))
        CubeListBox.files.insert(0, '../')
        #print(1, CubeListBox.paths, CubeListBox.files)
        return  # !

  def get_path(paths=[]):
      tmp_path = ''
      for p in CubeListBox.paths:
          tmp_path += p if p != '/' else ''
      return tmp_path

  process, state, selected, limit = 0, 1, 0, 4

  def on_draw():

    CubeListBox.btn.expand_event()

    if CubeListBox.btn.next() == 2:
        CubeListBox.selected = CubeListBox.selected - 1
        if CubeListBox.selected < 0:
            CubeListBox.selected = 0
            list_rshift(CubeListBox.files)

    elif CubeListBox.btn.back() == 2:
        CubeListBox.selected = CubeListBox.selected + 1

        real_len = CubeListBox.limit
        if len(CubeListBox.files) < real_len:
            real_len = len(CubeListBox.files)

        if CubeListBox.selected > real_len - 1:
            CubeListBox.selected = real_len - 1
            list_lshift(CubeListBox.files)

    elif CubeListBox.btn.home() == 2:
        tmp = CubeListBox.files[CubeListBox.selected]
        # if tmp == '/':
        #     raise Exception('exit CubeListBox...')
        if tmp in ["../"] or tmp.find('.') == -1:
            CubeListBox.load_explorer(tmp)
            #list_lshift(CubeListBox.files)
        else:
            CubeListBox.info = tmp

    ui.canvas.draw_string(10, 5, str(CubeListBox.get_path(CubeListBox.paths)), scale=1)

    ui.canvas.draw_string(10, 225, str(CubeListBox.info), scale=1)

    CubeListBox.process = CubeListBox.process + 1 % 24
    tmp = 5 * math.cos(CubeListBox.process * (math.pi / 12))

    view_len = len(CubeListBox.files)
    if view_len > CubeListBox.limit:
        view_len = CubeListBox.limit

    for i in range(view_len):
        pos = draw_dialog_alpha(ui.canvas, 20, int(tmp) + 40 + i * 50, 200, 20, 10, color=(0,255,0) if CubeListBox.selected == i else (255, 0, 0), alpha=255 - i * 30)
        ui.canvas.draw_string(pos[0] + 10, pos[1] + 10, CubeListBox.files[i], scale=2, color=(0,0,0))

if __name__ == "__main__":
    button_io.config(10, 11, 16) # cube
    CubeListBox.btn.Limit = 250
    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.grey_draw)
    @ui.warp_template(ui.bg_in_draw)
    #@ui.warp_template(ui.anime_in_draw)
    @ui.warp_template(CubeListBox.on_draw)
    def unit_test():
      ui.display()

    import time
    last = time.ticks_ms()
    while True:
        print(time.ticks_ms() - last)
        last = time.ticks_ms()
        # gc.collect()
        unit_test()
        try:
            print(time.ticks_ms() - last)
            last = time.ticks_ms()
            # gc.collect()
            unit_test()
        except Exception as e:
            print(e)
