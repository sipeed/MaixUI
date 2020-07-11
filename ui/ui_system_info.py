# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from ui_maix import ui

class system_info:

  info = 'this is test text.\n change to system_info.info'

  def info_draw():
    ui.img.draw_string(10, 120, system_info.info, color=(0, 255, 0), scale=2, mono_space=1)

if __name__ == "__main__":

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(system_info.info_draw)
    def unit_test():
      ui.display()

    import time
    while True:
        system_info.info = str(time.time())
        unit_test()
        time.sleep(1)

