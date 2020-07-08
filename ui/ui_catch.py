# debug file

from ui_maix import ui
from button import cube_button
import sys, image, lcd, time

def catch(func):
    def warp(warp=None):
        try:
            func()
        except Exception as e:
            try:
                btn = cube_button()

                import uio
                string_io = uio.StringIO()
                sys.print_exception(e, string_io)
                s = string_io.getvalue()
                ui.img.draw_rectangle(
                    (10, 10, 220, 220), fill=True, color=(50, 50, 50))
                msg = "** " + str(e)
                chunks, chunk_size = len(msg), 29
                msg_lines = [msg[i:i+chunk_size]
                             for i in range(0, chunks, chunk_size)]
                x_offset, y_offset = 10 + 5, 20
                ui.img.draw_string(
                    x_offset + 24, y_offset + 5, "A problem has been detected", color=(0, 255, 0))
                ui.img.draw_string(
                    x_offset + 3, y_offset + 16, "------------------------------", (255, 255, 255))

                current_y = y_offset + 10 + 5 + 16
                for line in msg_lines:
                    ui.img.draw_string(x_offset, current_y,
                                    line, color=(255, 0, 0))
                    current_y += 32
                    if current_y >= ui.img.height():
                        break

                ui.img.draw_string(x_offset, y_offset + current_y, s, color=(0, 255, 0))
                lcd.display(ui.img)

                happen = time.ticks_ms()
                while (happen + 5000) > time.ticks_ms():
                    info = "(%d)" % (
                        5 - (int)(time.ticks_ms() - happen) / 1000)
                    btn.event()
                    if btn.back() or btn.home() or btn.next():
                        break
                    ui.img.draw_rectangle(
                        (x_offset, y_offset + 5, len(info) * 8, 12), fill=True, color=(50, 50, 50))
                    ui.img.draw_string(x_offset, y_offset + 5, info, color=(0, 255, 0))
                    lcd.display(ui.img)
                    time.sleep_ms(100)
            except Exception as e:
                print(e)
    return warp


if __name__ == "__main__":

    from button import cube_button

    class test:

        btn = cube_button()

        info = 'this is test text.\n change to test.info'

        def info_draw():

            ui.img.draw_string(10, 120, test.info, scale=2, mono_space=1)

            if test.info != "working":
                test.info = "working"
                raise Exception(info_draw)

            test.btn.event()
            if test.btn.back() | test.btn.home() | test.btn.next():
                raise Exception(btn)

    @ui.warp_template(ui.bg_draw)
    @catch
    @ui.warp_template(test.info_draw)
    def unit_test():
      ui.display()

    import time
    while True:
      unit_test()
