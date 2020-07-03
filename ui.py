from core import Core

import lcd, time
import image

lcd.init(freq=15000000)

class ui:

    alpha = 1

    def Test():
        img.draw_image(image.Image("app_camera.jpg"), 20, 30, alpha=ui.alpha)
        # img.draw_image(image.Image("tmp.jpg"), 100, 30, alpha=250)
        lcd.display(img)
        ui.alpha += 5

Core.callback(ui.Test)

print('test')