import image
import lcd
import math
import gc

gc.collect()

lcd.init(freq=15000000)

def print_mem_free():
    print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')

class ui:

    alpha, img, logo, bak = 0, None, None, None

    def warp_template(func):
        def tmp_warp(warp=None):
            if warp:
              return lambda *args: [func(), warp()]
        return tmp_warp

    def bg_draw():
        gc.collect()
        if ui.bak == None:
            ui.bak = image.Image("/sd/res/images/bg.jpg") # 90ms
        ui.img = ui.bak.copy() # 10ms

    def help_draw():
        ui.img.draw_rectangle((0,0,240,240), fill=True, color=(0, 0, 0))
        ui.img.draw_string(30, 6, "<", (255, 0, 0), scale=2)
        ui.img.draw_string(60, 6, "ENTER/HOME", (255, 0, 0), scale=2)
        ui.img.draw_string(200, 6, ">", (255, 0, 0), scale=2)
        ui.img.draw_string(10, lcd.height() - 30, "RESET", (255, 0, 0), scale=2)
        ui.img.draw_string(178, lcd.height() - 30, "POWER", (255, 0, 0), scale=2)
        ui.logo_draw(255)

    def logo_draw(alpha = None):
        if alpha == None:
            alpha = math.cos(math.pi * ui.alpha / 24) * 50 + 150
            ui.alpha = (ui.alpha + 1) % 48
        if ui.logo == None:
            ui.logo = image.Image("/sd/res/images/logo.jpg") # 90ms
        tmp = ui.logo.copy() # 10ms
        ui.img.draw_image(tmp, 50, 50, alpha=int(alpha)) # 50ms
        del tmp

    def display():
        lcd.display(ui.img)
        del ui.img

if __name__ == "__main__":
    alpha = 0
    app_settings = image.Image("/sd/res/icons/app_settings.bmp") # 60ms
    app_explorer = image.Image("/sd/res/icons/app_explorer.bmp") # 60ms
    app_system_info = image.Image("/sd/res/icons/app_system_info.bmp") # 60ms
    app_camera = image.Image("/sd/res/icons/app_camera.bmp") # 60ms
    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(ui.help_draw)
    def test_launcher_draw():
         #print_mem_free()
        #lcd.display(ui.img) # 15ms
        ui.display()
        return
        ## print_mem_free()
        global alpha
        value = math.cos(math.pi * alpha / 12) * 100 + 100
        alpha = (alpha + 1) % 24
        #value = 255

        #tmp = image.Image("/sd/res/icons/app_camera.bmp") # 60ms
        tmp = app_camera.copy() # 1ms
        ui.img.draw_image(tmp, 40, 40, alpha=int(value)) # 4ms
        del tmp

        ui.img.draw_font(40 + 16, 40 + 70, 16, 16,
            b'\x08\x08\x08\x08\xFE\x08\x18\x1C\x2A\x2A\x48\x88\x08\x08\x08\x08\x00\xFC\x84\x84\x84\xFC\x84\x84\x84\xFC\x84\x84\x84\x84\xFC\x84'
            , scale=1, color=(0,255,0))
        ui.img.draw_font(40 + 36, 40 + 70, 16, 16,
            b'\x10\x11\x11\x11\xFD\x11\x31\x39\x55\x55\x91\x11\x11\x12\x12\x14\x00\xF0\x10\x10\x10\x10\x10\x10\x10\x10\x10\x12\x12\x12\x0E\x00'
            , scale=1, color=(0,255,0))

        tmp = app_system_info.copy() # 1ms
        #tmp = image.Image("/sd/res/icons/app_system_info.bmp") # 60ms
        ui.img.draw_image(tmp, 140, 40, alpha=int(value)) # 4ms
        del tmp

        ui.img.draw_font(140 + 16, 40 + 70, 16, 16,
            b'\x08\x08\x0B\x10\x10\x31\x30\x50\x91\x10\x10\x11\x11\x11\x11\x11\x40\x20\xFE\x00\x00\xFC\x00\x00\xFC\x00\x00\xFC\x04\x04\xFC\x04'
            , scale=1, color=(0,255,0))
        ui.img.draw_font(140 + 36, 40 + 70, 16, 16,
            b'\x01\x02\x1F\x10\x1F\x10\x1F\x10\x1F\x10\x01\x08\x48\x48\x87\x00\x00\x00\xF0\x10\xF0\x10\xF0\x10\xF0\x10\x00\x84\x92\x12\xF0\x00'
            , scale=1, color=(0,255,0))

        tmp = app_explorer.copy() # 1ms
        #tmp = image.Image("/sd/res/icons/app_explorer.bmp") # 60ms
        ui.img.draw_image(tmp, 140, 140, alpha=int(value)) # 4ms
        del tmp

        ui.img.draw_font(140 + 16, 140 + 70, 16, 16,
            b'\x01\x41\x21\x0A\x14\xE0\x21\x26\x1F\x10\x11\x11\x11\x02\x0C\x70\x00\x00\xFC\x44\x48\xA0\x10\x0C\xF0\x10\x10\x10\x10\x60\x18\x04'
            , scale=1, color=(0,255,0))
        ui.img.draw_font(140 + 36, 140 + 70, 16, 16,
            b'\x00\x27\x14\x14\x85\x45\x45\x15\x15\x25\xE4\x24\x29\x2A\x30\x00\x00\xFE\x20\x40\xFC\x04\xFC\x04\xFC\x24\x20\xA8\x24\x22\xA0\x40'
            , scale=1, color=(0,255,0))

        tmp = app_settings.copy() # 1ms
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
