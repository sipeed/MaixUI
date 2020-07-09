# This file is part of MaixUI
# Copyright (c) 2020 sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from core import Core

import lcd
import time
import image

lcd.init(freq=15000000)

alpha, img = 5, None

def bg_draw(warp=None):
    global img
    img = image.Image("/sd/res/images/bg.jpg")
    if warp:
        return lambda *args: warp()

def logo_draw(warp=None):
    global img, alpha
    img.draw_image(image.Image("/sd/res/images/logo.jpg"),
                   0, 0, alpha=255)
    if warp:
      return lambda *args: warp()

@logo_draw
@bg_draw
def test_draw():
    global img, alpha
    img.draw_image(image.Image("/sd/tmp.bmp"), alpha, alpha, alpha=alpha)
    alpha += 25
    lcd.display(img)

Core.callback(test_draw)
