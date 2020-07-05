
from test_launcher_draw import ui
from test_app_system_info import system_info

if __name__ == "__main__":
    @system_info.info_draw
    @ui.warp_template(ui.logo_draw)
    def app_main()
        print(app_main)
        lcd.display(ui.img)
    while True:
      app_main()
