# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#
import time, math

def get_time_curve(level=1, scope=500, func=math.sin):
    res = func(time.ticks_ms() / scope / math.pi)
    return pow(res, level) if level != 1 else res

if __name__ == "__main__":
            
    from dialog import draw_dialog_alpha
    from ui_canvas import ui, print_mem_free
    import time
    last = time.ticks_ms()

    while True:
        ui.blank_draw()
        ui.grey_draw()
        ui.bg_in_draw()

        #print(time.ticks_ms() - last)
        #last = time.ticks_ms()

        height = 50 + (int(get_time_curve(3, 250) * 40))
        pos = draw_dialog_alpha(ui.canvas, 20, height, 200, 20, 10, color=(255, 0, 0), alpha=150)
        ui.canvas.draw_string(pos[0] + 10, pos[1] + 10, "time_curve(3, 250)", scale=2, color=(0,0,0))

        height = 100 + (int(get_time_curve(2, 500) * 40))
        pos = draw_dialog_alpha(ui.canvas, 20, height, 200, 20, 10, color=(0, 255, 0), alpha=150)
        ui.canvas.draw_string(pos[0] + 10, pos[1] + 10, "time_curve(2, 500)", scale=2, color=(0,0,0))

        height = 150 + (int(get_time_curve(1, 100) * 40))
        pos = draw_dialog_alpha(ui.canvas, 20, height, 200, 20, 10, color=(0, 0, 255), alpha=150)
        ui.canvas.draw_string(pos[0] + 10, pos[1] + 10, "time_curve(1, 100)", scale=2, color=(0,0,0))

        ui.display()
