# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import image
import lcd
import math
import gc
import random

gc.collect()

lcd.init(freq=15000000)


def print_mem_free():
    print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')


class ui:

    alpha, img, anime, bak = 0, None, None, None

    bg_path = os.getcwd() + "/res/images/bg.jpg"
    logo_path = os.getcwd() + "/res/images/logo.jpg"

    height, weight = lcd.height(), lcd.width()

    def warp_template(func):
        def tmp_warp(warp=None):
            if warp:
              return lambda *args: [func(), warp()]
        return tmp_warp

    def blank_draw():
        ui.canvas = image.Image(size=(ui.height, ui.weight)
                                )  # 50ms # 168.75kb (112kb)

    def grey_draw():
        ui.blank_draw()
        ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight),
                                 fill=True, color=(75, 75, 75))

    def bg_in_draw():
        #ui.canvas.draw_rectangle((0, 0, ui.height, ui.weight),
                                 #fill=True, color=(75, 75, 75))
        #if ui.bak == None:
        #ui.bak.draw_rectangle((60,30,120,150), fill=True, color=(250, 0, 0))
        #ui.bak.draw_string(70, 40, "o", color=(255, 255, 255), scale=2)
        #ui.bak.draw_string(80, 10, "s", color=(255, 255, 255), scale=15)
        ui.canvas.draw_circle(120, 120, int(50), fill=True,
                              color=(250, 0, 0))  # 10ms
        ui.canvas.draw_string(100, 88, "o", color=(255, 255, 255), scale=1)
        ui.canvas.draw_string(103, 70, "s", color=(255, 255, 255), scale=8)
        # ui.canvas = ui.canvas # 15ms
        #ui.canvas = ui.bak.copy() # 10ms 282kb

    def bg_draw():
        gc.collect()
        if ui.bak == None:
            ui.bak = image.Image(ui.bg_path)  # 90ms
        ui.canvas = ui.bak.copy()  # 10ms

    def help_in_draw():
        ui.canvas.draw_string(30, 6, "<", (255, 0, 0), scale=2)
        ui.canvas.draw_string(60, 6, "ENTER/HOME", (255, 0, 0), scale=2)
        ui.canvas.draw_string(200, 6, ">", (255, 0, 0), scale=2)
        ui.canvas.draw_string(10, ui.height - 30,
                              "RESET", (255, 0, 0), scale=2)
        ui.canvas.draw_string(178, ui.height - 30,
                              "POWER", (255, 0, 0), scale=2)

    def help_draw():
        ui.canvas.draw_rectangle((0, 0, 240, 240), fill=True, color=(0, 0, 0))
        ui.canvas.draw_string(30, 6, "<", (255, 0, 0), scale=2)
        ui.canvas.draw_string(60, 6, "ENTER/HOME", (255, 0, 0), scale=2)
        ui.canvas.draw_string(200, 6, ">", (255, 0, 0), scale=2)
        ui.canvas.draw_string(10, ui.height - 30,
                              "RESET", (255, 0, 0), scale=2)
        ui.canvas.draw_string(178, ui.height - 30,
                              "POWER", (255, 0, 0), scale=2)
        ui.anime_draw(255)
        del ui.anime
        ui.anime = None

    def anime_draw(alpha=None):
        if alpha == None:
            alpha = math.cos(math.pi * ui.alpha / 32) * 50 + 180
            ui.alpha = (ui.alpha + 1) % 64
        if ui.anime == None:
            ui.anime = image.Image(ui.logo_path)  # 90ms
        tmp = ui.anime.copy()  # 10ms
        ui.canvas.draw_image(tmp, 50, 50, alpha=int(alpha))  # 50ms
        del tmp

    def anime_in_draw(alpha=None):
        if alpha == None:
            alpha = math.cos(math.pi * ui.alpha / 100) * 200
            ui.alpha = (ui.alpha + 1) % 200
        r, g, b = random.randint(120, 255), random.randint(
            120, 255), random.randint(120, 255)
        ui.canvas.draw_circle(0, 0, int(alpha), color=(
            r, g, b), thickness=(r % 5))  # 10ms
        ui.canvas.draw_circle(0, 0, 200 - int(alpha),
                              color=(r, g, b), thickness=(g % 5))  # 10ms

        ui.canvas.draw_circle(240, 0, int(alpha), color=(
            r, g, b), thickness=(b % 5))  # 10ms
        ui.canvas.draw_circle(240, 0, 200 - int(alpha),
                              color=(r, g, b), thickness=(r % 5))  # 10ms

        ui.canvas.draw_circle(0, 240, int(alpha), color=(
            r, g, b), thickness=(g % 5))  # 10ms
        ui.canvas.draw_circle(0, 240, 200 - int(alpha),
                              color=(r, g, b), thickness=(b % 5))  # 10ms

        ui.canvas.draw_circle(240, 240, int(alpha), color=(
            r, g, b), thickness=(r % 5))  # 10ms
        ui.canvas.draw_circle(240, 240, 200 - int(alpha),
                              color=(r, g, b), thickness=(g % 5))  # 10ms

    def display():  # 10ms
        lcd.display(ui.canvas)
        del ui.canvas
        gc.collect()


if __name__ == "__main__":
    @ui.warp_template(ui.grey_draw)
    @ui.warp_template(ui.bg_in_draw)
    #@ui.warp_template(ui.anime_draw)
    def test_launcher_draw():
        ui.display()
        print_mem_free()

    import time
    last = time.ticks_ms()
    while True:
        try:
            print(time.ticks_ms() - last)
            last = time.ticks_ms()
            test_launcher_draw()
        except Exception as e:
            gc.collect()
            print(e)
