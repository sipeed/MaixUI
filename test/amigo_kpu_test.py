
import sensor, image, time, lcd

from machine import I2C
import lcd, utime
from fpioa_manager import fm
from Maix import GPIO
import KPU as kpu


class AXP173:
    class PMUError(Exception):
        pass
    class OutOfRange(PMUError):
        pass
    def __init__(self, i2c_dev=None, i2c_addr=0x34):
        from machine import I2C
        if i2c_dev is None:
            try:
                self.i2cDev = I2C(I2C.I2C0, freq=400000, scl=24, sda=27)
            except Exception:
                raise PMUError("Unable to init I2C0 as Master")
        else:
            self.i2cDev = i2c_dev
        self.i2cDev.scan()
        self.axp173Addr = i2c_addr
    def __write_reg(self, reg_address, value):
        self.i2cDev.writeto_mem(
            self.axp173Addr, reg_address, value, mem_size=8)
    def writeREG(self, regaddr, value):
        self.__write_reg(regaddr, value)

i2cDev = I2C(I2C.I2C0, freq=400000, scl=24, sda=27)
print(i2cDev.scan())

axp173 = AXP173()
axp173.writeREG(0x27, 0x20)
axp173.writeREG(0x28, 0x0C)

lcd.init()

clock = time.clock()
#sensor.reset(choice=1, dual_buff=True)
sensor.reset(choice=1)
sensor.set_pixformat(sensor.YUV422)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.skip_frames(time=2000)
#sensor.set_windowing((448, 448))
sensor.run(1)

#lcd.clear()
#sensor.set_windowing((224, 224))
#lcd.draw_string(100, 96, "MobileNet Demo")
#lcd.draw_string(100, 112, "Loading labels...")
#f = open('labels.txt', 'r')
#labels = f.readlines()
#f.close()
#kpu.memtest()
#task = kpu.load(0x720000)
#kpu.memtest()
#clock = time.clock()
#while(True):
        #img = sensor.snapshot()#.resize(224, 224)
        #a = lcd.display(img, oft=(0, 0))
        ##tmp = img.cut(48, 8, 224, 224)
        ##tmp = img.resize(224, 224)
        #img.pix_to_ai()
        #clock.tick()
        #try:
            #fmap = kpu.forward(task, img)
            ##print(fmap)
            #plist = fmap[:]
            #pmax = max(plist)
            #max_index = plist.index(pmax)
            #lcd.draw_string(0, 224 + 12, "%.2f:%s                            " %
                            #(pmax, labels[max_index].strip()))
        #except Exception as e:
            #print(e)
        #print(clock.fps())
#a = kpu.deinit(task)

#task = kpu.load(0x2C0000) # you need put model(face.kfpkg) in flash at address 0x300000
##task = kpu.load("/sd/0x2C0000_facedetect.kmodel")
#anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
#a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

#task = kpu.load(0x5C0000)
#classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
##task = kpu.load("/sd/0x5C0000_20class.kmodel")
#anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
#a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

'''
fm.register(23, fm.fpioa.GPIOHS0)
key_gpio = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)

start_processing = False

def set_key_state(*_):
    global start_processing
    start_processing = True

key_gpio.irq(set_key_state, GPIO.IRQ_RISING, GPIO.WAKEUP_NOT_SUPPORT)

kpu.memtest()
try:
    while(True):
        clock.tick()
        #print(time.ticks_ms())
        img = sensor.snapshot()
        #lcd.display(img)
        #tmp = img.cut(80, 40, 320, 240)
        tmp = img.resize(320, 240)
        tmp.pix_to_ai()
        #print(img)
        #img.rotation_corr(y_rotation = 180)
        code = kpu.run_yolo2(task, tmp)
        if code:
            for pos in range(len(code)):
                i = code[pos]
            #for i in code:
                #print(i)
                color = (255, 255, 255)
                if start_processing:
                    if pos == 2:
                        color = (0, 255, 0)
                        img.draw_string(i.x()*2, i.y()*2 - 40, "target", scale=3, color=color)
                    if len(code) == 1:
                        color = (0, 255, 0)
                        img.draw_string(i.x()*2, i.y()*2 - 40, "target", scale=3, color=color)
                img.draw_rectangle(i.x()*2, i.y()*2, i.w() * 2, i.h() * 2, thickness=5, color=color)
                #img.draw_rectangle(320 - (i.x() + i.w()), i.y(), i.w(), i.h())

                #img.draw_rectangle(i.x()*2, i.y()*2, i.w() * 2, i.h() * 2)
                #img.draw_string(0, 400, '%.2f:%s' % (i.value(), classes[i.classid()]), scale=5)

        lcd.display(img.resize(480, 320))
        print(clock.fps())
        #print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')
except KeyboardInterrupt as e:
    print(e)
    kpu.deinit(task)

'''

#path = "/flash/tack_picture.jpeg"

##img = sensor.snapshot()
##print("save image")
##img.save(path)

#print("read image")
#img = image.Image(path)
#lcd.display(img)
#print("ok")

'''
kpu.memtest()
task_fd = kpu.load(0x2C0000)
task_ld = kpu.load(0x580000)
task_fe = kpu.load(0x340000)
kpu.memtest()
clock = time.clock()

fm.register(23, fm.fpioa.GPIOHS0)
key_gpio = GPIO(GPIO.GPIOHS0, GPIO.IN)
start_processing = False


def set_key_state(*_):
    global start_processing
    start_processing = True

key_gpio.irq(set_key_state, GPIO.IRQ_RISING, GPIO.WAKEUP_NOT_SUPPORT)

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437,
          6.92275, 6.718375, 9.01025)  # anchor for face detect
dst_point = [(44, 59), (84, 59), (64, 82), (47, 105),
             (81, 105)]  # standard face key point position
a = kpu.init_yolo2(task_fd, 0.5, 0.3, 5, anchor)
img_lcd = image.Image(size=(480, 320))
img_face = image.Image(size=(128, 128))
a = img_face.pix_to_ai()
record_ftr = []
record_ftrs = []
names = ['Mr.1', 'Mr.2', 'Mr.3', 'Mr.4', 'Mr.5',
         'Mr.6', 'Mr.7', 'Mr.8', 'Mr.9', 'Mr.10']
kpu.memtest()
while(1):
    try:
        img_lcd.clear()
        img = sensor.snapshot()
        clock.tick()
        a = img.pix_to_ai()
        #a = img.pix_to_ai()
        code = kpu.run_yolo2(task_fd, img)
        if code:
            #for i in code:
            for pos in range(len(code)):
                i = code[pos]
                # print(i)
                # Cut face and resize to 128x128
                a = img.draw_rectangle(i.x(), i.y(), i.w(), i.h())
                face_cut = img.cut(i.x(), i.y(), i.w(), i.h())
                face_cut_128 = face_cut.resize(128, 128)
                a = face_cut_128.pix_to_ai()
                a = img_lcd.draw_image(face_cut_128, (320,0))
                #print(i)

                # Landmark for face 5 points
                fmap = kpu.forward(task_ld, face_cut_128)
                plist = fmap[:]
                le = (int(i.x() + plist[0]*i.w() - 10), int(i.y() + plist[1]*i.h()))
                re = (int(i.x() + plist[2]*i.w()), int(i.y() + plist[3]*i.h()))
                nose = (int(i.x() + plist[4]*i.w()), int(i.y() + plist[5]*i.h()))
                lm = (int(i.x() + plist[6]*i.w()), int(i.y() + plist[7]*i.h()))
                rm = (int(i.x() + plist[8]*i.w()), int(i.y() + plist[9]*i.h()))
                #print(le, re, nose, lm, rm)
                a = img.draw_circle(int(le[0]), int(le[1]), 4)
                a = img.draw_circle(int(re[0]), int(re[1]), 4)
                a = img.draw_circle(int(nose[0]), int(nose[1]), 4)
                a = img.draw_circle(int(lm[0]), int(lm[1]), 4)
                a = img.draw_circle(int(rm[0]), int(rm[1]), 4)
                # align face to standard position
                src_point = [le, re, nose, lm, rm]
                T = image.get_affine_transform(src_point, dst_point)
                a = image.warp_affine_ai(img, img_face, T)
                a = img_face.ai_to_pix()
                a = img_lcd.draw_image(img_face, (320,128))
                del(face_cut_128)

                # calculate face feature vector
                fmap = kpu.forward(task_fe, img_face)
                feature = kpu.face_encode(fmap[:])
                reg_flag = False
                scores = []
                for j in range(len(record_ftrs)):
                    score = kpu.face_compare(record_ftrs[j], feature)
                    scores.append(score)
                max_score = 0
                index = 0
                for k in range(len(scores)):
                    if max_score < scores[k]:
                        max_score = scores[k]
                        index = k
                if max_score > 85:
                    a = img.draw_string(i.x(), i.y(), ("%s :%2.1f" % (
                        names[index], max_score)), color=(0, 255, 0), scale=2)
                    a = img_lcd.draw_string(80 * (pos % 3), 240 + 30 * (pos // 3), ("%s :%2.1f" % (
                        names[index], max_score)), color=(0, 255, 0), scale=2)
                else:
                    a = img.draw_string(i.x(), i.y(), ("X :%2.1f" % (
                        max_score)), color=(255, 0, 0), scale=2)
                    a = img_lcd.draw_string(80 * (pos % 3), 240 + 30 * (pos // 3), ("X :%2.1f" % (
                        max_score)), color=(255, 0, 0), scale=2)
                if start_processing:
                    record_ftr = feature
                    record_ftrs.append(record_ftr)
                    start_processing = False

                #break
        fps = clock.fps()
        print("%2.1f fps" % fps)
        img_lcd.draw_image(img, (0,0))
        a = lcd.display(img_lcd) #.resize(480, 320)
        gc.collect()
        kpu.memtest()
    except KeyboardInterrupt as e:
        a = kpu.deinit(task_fe)
        a = kpu.deinit(task_ld)
        a = kpu.deinit(task_fd)
        print(e)
    except Exception as e:
        print(e)
    #break
'''
