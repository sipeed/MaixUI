import math
from maix_ui import ui
from ui_taskbar import taskbar

class launcher:
    alpha = 0
    app_settings = image.Image("/sd/res/icons/app_settings.bmp") # 60ms
    app_explorer = image.Image("/sd/res/icons/app_explorer.bmp") # 60ms
    app_system_info = image.Image("/sd/res/icons/app_system_info.bmp") # 60ms
    app_camera = image.Image("/sd/res/icons/app_camera.bmp") # 60ms

    @ui.warp_template(ui.logo_draw)
    @ui.warp_template(taskbar.time_draw)
    def event():
         #print_mem_free()
        #lcd.display(ui.img) # 15ms
        #return
        ## print_mem_free()
        value = math.cos(math.pi * launcher.alpha / 12) * 90 + 160
        launcher.alpha = (launcher.alpha + 1) % 24
        #value = 255

        #tmp = image.Image("/sd/res/icons/app_camera.bmp") # 60ms
        tmp = launcher.app_camera.copy() # 1ms
        ui.img.draw_image(tmp, 40, 40, alpha=int(value)) # 4ms
        del tmp

        ui.img.draw_font(40 + 16, 40 + 70, 16, 16,
            b'\x08\x08\x08\x08\xFE\x08\x18\x1C\x2A\x2A\x48\x88\x08\x08\x08\x08\x00\xFC\x84\x84\x84\xFC\x84\x84\x84\xFC\x84\x84\x84\x84\xFC\x84'
            , scale=1, color=(0,255,0))
        ui.img.draw_font(40 + 36, 40 + 70, 16, 16,
            b'\x10\x11\x11\x11\xFD\x11\x31\x39\x55\x55\x91\x11\x11\x12\x12\x14\x00\xF0\x10\x10\x10\x10\x10\x10\x10\x10\x10\x12\x12\x12\x0E\x00'
            , scale=1, color=(0,255,0))

        tmp = launcher.app_system_info.copy() # 1ms
        #tmp = image.Image("/sd/res/icons/app_system_info.bmp") # 60ms
        ui.img.draw_image(tmp, 140, 40, alpha=int(value)) # 4ms
        del tmp

        ui.img.draw_font(140 + 16, 40 + 70, 16, 16,
            b'\x08\x08\x0B\x10\x10\x31\x30\x50\x91\x10\x10\x11\x11\x11\x11\x11\x40\x20\xFE\x00\x00\xFC\x00\x00\xFC\x00\x00\xFC\x04\x04\xFC\x04'
            , scale=1, color=(0,255,0))
        ui.img.draw_font(140 + 36, 40 + 70, 16, 16,
            b'\x01\x02\x1F\x10\x1F\x10\x1F\x10\x1F\x10\x01\x08\x48\x48\x87\x00\x00\x00\xF0\x10\xF0\x10\xF0\x10\xF0\x10\x00\x84\x92\x12\xF0\x00'
            , scale=1, color=(0,255,0))

        tmp = launcher.app_explorer.copy() # 1ms
        #tmp = image.Image("/sd/res/icons/app_explorer.bmp") # 60ms
        ui.img.draw_image(tmp, 140, 140, alpha=int(value)) # 4ms
        del tmp

        ui.img.draw_font(140 + 16, 140 + 70, 16, 16,
            b'\x01\x41\x21\x0A\x14\xE0\x21\x26\x1F\x10\x11\x11\x11\x02\x0C\x70\x00\x00\xFC\x44\x48\xA0\x10\x0C\xF0\x10\x10\x10\x10\x60\x18\x04'
            , scale=1, color=(0,255,0))
        ui.img.draw_font(140 + 36, 140 + 70, 16, 16,
            b'\x00\x27\x14\x14\x85\x45\x45\x15\x15\x25\xE4\x24\x29\x2A\x30\x00\x00\xFE\x20\x40\xFC\x04\xFC\x04\xFC\x24\x20\xA8\x24\x22\xA0\x40'
            , scale=1, color=(0,255,0))

        tmp = launcher.app_settings.copy() # 1ms
        #tmp = image.Image("/sd/res/icons/app_settings.bmp") # 60ms
        ui.img.draw_image(tmp, 40, 140, alpha=int(value)) # 4ms
        del tmp

        ui.img.draw_font(40 + 16, 140 + 70, 16, 16,
            b'\x00\x21\x11\x11\x01\x02\xF4\x13\x11\x11\x10\x14\x18\x10\x03\x0C\x00\xF0\x10\x10\x10\x0E\x00\xF8\x08\x10\x90\xA0\x40\xA0\x18\x06'
            , scale=1, color=(0,255,0))
        ui.img.draw_font(40 + 36, 140 + 71, 16, 16,
            b'\x7F\x44\x7F\x01\x7F\x01\x1F\x10\x1F\x10\x1F\x10\x1F\x10\xFF\x00\xFC\x44\xFC\x00\xFC\x00\xF0\x10\xF0\x10\xF0\x10\xF0\x10\xFE\x00'
            , scale=1, color=(0,255,0))

        ## print_mem_free()

        ui.display()

if __name__ == "__main__":

    import time
    while True:
        launcher.event()

