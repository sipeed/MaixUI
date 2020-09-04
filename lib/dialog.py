
import image

def draw_fillet(img, topL, topR, downL, downR, radius, fill=True, color=(255, 0, 0)):
    #print(topL, topR, downL, downR, radius)
    t, r = 6, t // 2
    topL[0], topL[1] = topL[0] + r, topL[1] + r
    topR[0], topR[1] = topR[0] + r, topL[1] + r
    downL[0], downR[1] = downL[0] + r, downR[1] + r
    topL[0], topL[1] = topL[0] + r, topL[1] + r
    tmp = [
      (topL[0] + radius, topL[1] - radius),
      (topR[0] - radius, topR[1] - radius),
      (topR[0] + radius, topR[1] + radius),
      (downR[0] + radius, downR[1] - radius),
      (downR[0] - radius, downR[1] + radius),
      (downL[0] + radius, downL[1] + radius),
      (downL[0] - radius, downL[1] - radius),
      (topL[0] - radius, topL[1] + radius),
    ]
    for i in range(-1, len(tmp) - 1):
        img.draw_line(tmp[i][0], tmp[i][1], tmp[i+1][0], tmp[i+1][1], thickness=t, color=color)
        #img.draw_line(tmp[i][0], tmp[i][1], tmp[i+1][0], tmp[i+1][1], color=0)

    if fill:
        img.flood_fill(topL[0] + 5, topL[1] + 5, \
            seed_threshold=0.05, floating_thresholds=0.05, \
            color=color, invert=False, clear_background=False)

    img.draw_circle(topL[0] + radius, topL[1] + radius, radius*2, fill=False, color=color)
    img.draw_circle(topR[0] - radius, topR[1] + radius, radius*2, fill=False, color=color)
    img.draw_circle(downL[0] + radius, downL[1] - radius, radius*2, fill=False, color=color)
    img.draw_circle(downR[0] - radius, downR[1] - radius, radius*2, fill=False, color=color)

def draw_dialog_fast(img, x, y, w, h, radius=0, color=(255, 0, 0), alpha=255):
    if radius == 0:
        radius = h // 2
    draw_fillet(img, (x, y), (x + w, y), (x, y + h), (x + w, y + h), radius, color=color)

def draw_dialog_alpha(img, x, y, w, h, radius=0, color=(255, 0, 0), alpha=255):
    if radius == 0:
        radius = h // 2
    bak = image.Image(size=(w + 2*radius, h + 2*radius))
    #draw_fillet(bak, (radius, radius), (radius+ w, radius), (radius, radius+ h), (radius+ w, radius+ h), radius - 7, False, color=(255, 255, 255))
    draw_fillet(bak, (radius, radius), (radius+ w, radius), (radius, radius+ h), (radius+ w, radius+ h), radius + 1, False, color=color)
    img.draw_image(bak, x - radius, y - radius, alpha=alpha)
    del bak
    return (x - radius, y - radius)
    #img.draw_rectangle(x - radius, y - radius, w + 2*radius, h + 2*radius, color=color, fill=False)

if __name__ == "__main__":

    import lcd, time, math, random

    lcd.init()

    value = 0

    while True:

        height = int(math.cos(math.pi * value / 16) * 40 + 100)
        value = (value + 1) % 32

        img = image.Image(size=(240, 240))
        img.draw_rectangle(0, 0, 240, 240, color=(30, 30, 30), fill=True)
        for i in range(4):
            draw_dialog_fast(img, 20, 30 + i * 50, 200, 30, 5, color=(200 - i * 30, 200 - i * 30, 200 - i * 30))

        img.draw_string(0, 120, "this is test", scale=4, color=(0, 255, 0))

        x, y, w, h = 40, height, 160, 50

        pos = draw_dialog_alpha(img, x, y, w, h, 10, alpha=200)
        img.draw_string(pos[0] + 10, pos[1] + 10, "dialog A\n" + str(time.ticks_ms() // 1000), scale=2, color=(0,0,0))

        pos = draw_dialog_alpha(img, x + 20, 40, w, h, 10, color=(0, 0, 255), alpha=200)
        img.draw_string(pos[0] + 10, pos[1] + 10, "dialog B\n" + str(time.ticks_ms() // 1000), scale=2, color=(0,0,0))

        lcd.display(img)


