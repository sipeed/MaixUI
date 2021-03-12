# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#
try:
    from fs import OS
except:
    from driver.fs import OS

class photos:

    image_pos = 0
    image_set = []

    def scan(path=['/sd/imgs','/flash/imgs']): # '/sd/imgs',
        images = {}
        for p in path:
            try:
                images[p] = OS.listdir(p)
            except Exception as e:
                print(e, p)
                # gc.collect()
        photos.image_set = []
        for path in images:
            for file in images[path]:
                photos.image_set.append(path + '/' + file)
        print(photos.image_set)

    def image_next():
        if len(photos.image_set) > 0:
            photos.image_pos = (photos.image_pos + 1) % len(photos.image_set)

    def image_last():
        if len(photos.image_set) > 0:
            photos.image_pos = (photos.image_pos - 1) % len(photos.image_set)

    def image_path():
        if len(photos.image_set) > 0:
            #print(photos.image_set, photos.image_pos)
            return photos.image_set[photos.image_pos]
        return ''

    def photos_len():
        return len(photos.image_set)

    def unit_test():
        import lcd
        photos.scan()
        for i in range(len(photos.image_set) + 2):
            img = image.Image(photos.image_path())
            lcd.display(img)
            del img
            time.sleep(0.5)
            photos.image_next()

        for i in range(len(photos.image_set) + 2):
            img = image.Image(photos.image_path())
            lcd.display(img)
            del img
            time.sleep(0.5)
            photos.image_last()

if __name__ == "__main__":
    photos.unit_test()