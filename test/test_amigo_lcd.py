
import lcd, image, gc

lcd.init()
lcd.direction(0b01001000) # 480H * 320W Top-left

if __name__ == "__main__":
  gc.collect()
  print(gc.mem_free() / 1024, 'kb')
  bak = gc.mem_free()
  img = image.Image(size=(lcd.width(), lcd.height()))
  print((bak - gc.mem_free()) / 1024)
  img.draw_rectangle(0,   0, int(lcd.width() / 2), int(lcd.height() / 2), fill=True, color=(255, 0, 0))
  #img.draw_rectangle(60,  0,  480, 160, fill=True, color=(0, 255, 0))
  #img.draw_rectangle(120, 0,  480, 240, fill=True, color=(0, 0, 255))
  info = "[width:height]\n[{}:{}]".format(lcd.width(),lcd.height())

  img.draw_string(0, int(lcd.height() / 2), info,
                          color=(0, 255, 0), scale=2, mono_space=1)

  lcd.display(img)
  del img
  print(gc.mem_free() / 1024, 'kb')
  gc.collect()

  img = image.Image('/sd/test.jpg')
  lcd.display(img)
  print(gc.mem_free() / 1024, 'kb')
