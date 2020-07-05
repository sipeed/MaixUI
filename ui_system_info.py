
from maix_ui import ui

class system_info:

  info = 'test'

  def info_draw1():
    ui.img.draw_string(40, 40, 'system_info.info_draw1\n this is test text.')

  def info_draw2():
    ui.img.draw_string(40, 80, 'system_info.info_draw2\n maybe you need help?')

  @ui.warp_template(ui.bg_draw)
  @ui.warp_template(info_draw1)
  def app_system_info_main1():
      ui.display()

  @ui.warp_template(ui.logo_draw)
  @ui.warp_template(info_draw2)
  def app_system_info_main2():
      ui.display()

if __name__ == "__main__":

    import time
    while True:
        system_info.app_system_info_main1()
        time.sleep(2)
        system_info.app_system_info_main2()
        time.sleep(2)

