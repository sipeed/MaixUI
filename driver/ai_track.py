# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from ui_canvas import ui
import camera

class find_color():

    is_load = False

    red_threshold = (53, 31, 44, 82, 18, 78)
    area = (0, 0, 480, 320)
    blobs = None

    # search max blob
    def search_max(blobs):
        max_blob = 0
        max_size = 0
        for blob in blobs:
            blob_area = blob[2] * blob[3]
            if blob_area > max_size:
                max_blob = blob
                max_size = blob_area
        return max_blob

    # Find the largest circle position in the frame
    def search_max_circle(ball_threshold, area, img):
        #clock.tick()  # Track elapsed milliseconds between snapshots().
          # Take a picture and return the image.
        find_color.blobs = img.find_blobs([ball_threshold], roi=area)
        #print(blobs)
        if find_color.blobs:
            max_blob = find_color.search_max(find_color.blobs)
            x = max_blob[0] - 3
            y = max_blob[1] - 3
            w = max_blob[2] + 6
            h = max_blob[3] + 6
            outside_rect = (x, y, w, h)
            #print(max_blob)
            #print("fps:", clock.fps())
            img.draw_rectangle(max_blob[0:4])  # rect
            img.draw_rectangle(outside_rect[0:4])  # rect
            img.draw_cross(max_blob[5], max_blob[6]) # cx,cy


    def load():
        if find_color.is_load == False:
            #print(find_color.load)
            find_color.is_load = True

    def work(img):
        #print(find_color.work)
        #img.draw_string(20, 240, 'Find Max Red Color', (255, 0, 0), scale=2)
        find_color.search_max_circle(find_color.red_threshold, find_color.area, img)

        return img

    def free():
        if find_color.is_load:
            #print(find_color.free)
            find_color.is_load = False

if __name__ == "__main__":

    ui.height, ui.weight = 480, 320
    def test_ai_camera():

        @ui.warp_template(ui.blank_draw)
        def app_main():
            tmp = camera.obj.get_image()
            find_color.work(tmp)
            ui.canvas.draw_image(tmp, 0, 0)
            ui.display()

        import time
        last = time.ticks_ms()
        while True:
            find_color.load()
            try:
                print(time.ticks_ms() - last)
                last = time.ticks_ms()
                app_main()
            except Exception as e:
                # gc.collect()
                print(e)
            find_color.free()

    test_ai_camera()

