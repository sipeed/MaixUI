# -*- coding: UTF-8 -*-

class NeedRebootException(Exception):
    pass

class BaseApp:
    def __init__(self, system):
        print("BaseApp.__init__ called")
        self.system = system

    def on_draw(self):
        pass

    def on_back_pressed(self):
        # not handled by default
        return False

    def on_home_button_changed(self, state):
        return False

    def on_top_button_changed(self, state):
        return False

    def invalidate_drawing(self):
        self.system.invalidate_drawing()

    def get_system(self):
        return self.system

    def app_periodic_task(self):
        pass
