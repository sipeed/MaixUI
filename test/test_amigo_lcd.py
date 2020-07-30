
import lcd, image, gc, time

#lcd.init(type=1, width=480, height=320, freq=20000000)
#lcd.direction(0xA8)#修改颜色模式
lcd.init()
#lcd.direction(0x18) # 以 左上为原点。

# usage Maix.u + tab + gc_heap 0x100000.

if __name__ == "__main__":
    while True:
        gc.collect()
        print(gc.mem_free() / 1024, 'kb')
        bak = gc.mem_free()
        img = image.Image("/sd/tmp.jpeg") # size=(lcd.width(), lcd.height())
        print((bak - gc.mem_free()) / 1024)
        #img.draw_rectangle(0,   0,  100, 80, fill=True, color=(255, 0, 0))
        #img.draw_rectangle(60,  0,  480, 160, fill=True, color=(0, 255, 0))
        #img.draw_rectangle(120, 0,  480, 480, fill=True, color=(0, 0, 255))
        #img.draw_string(320, 480, "lcd[{}:{}]".format(lcd.width(), lcd.height()))
        lcd.display(img)
        del img
        print(gc.mem_free() / 1024, 'kb')
        gc.collect()
        time.sleep(1)
        gc.collect()
        print(gc.mem_free() / 1024, 'kb')
        bak = gc.mem_free()
        img = image.Image("/sd/test.jpg") # size=(lcd.width(), lcd.height())
        print((bak - gc.mem_free()) / 1024)
        #img.draw_rectangle(0,   0,  100, 80, fill=True, color=(255, 0, 0))
        #img.draw_rectangle(60,  0,  480, 160, fill=True, color=(0, 255, 0))
        #img.draw_rectangle(120, 0,  480, 480, fill=True, color=(0, 0, 255))
        #img.draw_string(320, 480, "lcd[{}:{}]".format(lcd.width(), lcd.height()))
        lcd.display(img)
        del img
        print(gc.mem_free() / 1024, 'kb')
        gc.collect()
        time.sleep(1)

