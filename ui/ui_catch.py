# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#


try:
    from ui_canvas import ui
    from button import sipeed_button
except ImportError:
    from ui.ui_canvas import ui
    from driver.button import sipeed_button

import sys
import image
import lcd
import time
import gc


def catch(func):
    def warp(warp=None):
        try:
            func()
        except Exception as e:
            try:
                btn = sipeed_button()

                import uio
                string_io = uio.StringIO()
                sys.print_exception(e, string_io)
                s = string_io.getvalue()
                ui.canvas.draw_rectangle(
                    (10, 10, ui.height - 20, ui.weight - 20), fill=True, color=(50, 50, 50))
                msg = "** " + str(e)
                chunks, chunk_size = len(msg), 29
                msg_lines = [msg[i:i+chunk_size]
                             for i in range(0, chunks, chunk_size)]
                x_offset, y_offset = 10 + 5, 20
                ui.canvas.draw_string(
                    x_offset + 24, y_offset + 5, "A problem has been detected", color=(0, 255, 0))
                ui.canvas.draw_string(
                    x_offset + 3, y_offset + 16, "------------------------------", (255, 255, 255))

                current_y = y_offset + 10 + 5 + 16
                for line in msg_lines:
                    ui.canvas.draw_string(x_offset, current_y,
                                          line, color=(255, 0, 0))
                    current_y += 16
                    if current_y >= ui.canvas.height():
                        break

                ui.canvas.draw_string(
                    x_offset, y_offset + current_y, s, color=(0, 255, 0))
                lcd.display(ui.canvas)

                happen = time.ticks_ms()
                while (happen + 5000) > time.ticks_ms():
                    info = "(%d)" % (
                        5 - (int)(time.ticks_ms() - happen) / 1000)
                    btn.event()
                    if btn.back() == 2 or btn.home() == 2 or btn.next() == 2:
                        break
                    ui.canvas.draw_rectangle(
                        (x_offset, y_offset + 5, len(info) * 8, 12), fill=True, color=(50, 50, 50))
                    ui.canvas.draw_string(
                        x_offset, y_offset + 5, info, color=(0, 255, 0))
                    lcd.display(ui.canvas)
                    time.sleep_ms(100)
                ui.display()
                # gc.collect()
            except Exception as e:
                print(e)
    return warp


if __name__ == "__main__":

    class test:

        btn = sipeed_button()

        info = 'this is test text.\n change to test.info'

        def info_draw():

            ui.canvas.draw_string(10, 120, test.info, scale=2, mono_space=1)

            if test.info != "working":
                test.info = "working"
                raise Exception(info_draw)

            test.btn.event()
            if test.btn.back() | test.btn.home() | test.btn.next():
                raise Exception(btn)

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(ui.bg_in_draw)
    @catch
    @ui.warp_template(test.info_draw)
    def unit_test():
      ui.display()

    import time
    while True:
      unit_test()
