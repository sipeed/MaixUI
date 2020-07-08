from Maix import GPIO
from board import board_info
from fpioa_manager import fm
import lcd
import machine
import sys
import image
import gc
import time
import os
os.listdir()
import resource
import config
from driver_mpu_axp173 import AXP173
from framework import NeedRebootException
from app_launcher import LauncherApp
Buttom_BACK_IO  = 11
Buttom_ENTER_IO = 10
Buttom_NEXT_IO  = 16
LED_R_IO = 13
LED_G_IO = 12
LED_B_IO = 14
class MaixCubeSystem:
	def __init__(self):
		self.pmu = AXP173()
		self.app_stack = []
		lcd.init()
		lcd.rotation(2)
		self.home_button = None
		self.back_button = None
		self.next_button = None
		self.home_button_state = False
		self.back_button_state = False
		self.next_button_state = False
		self.led_w = None
		self.led_r = None
		self.led_g = None
		self.led_b = None
		self.spk_sd = None
		self.is_handling_irq = False
		self.init_fm()
		self.is_drawing_dirty = False
		self.is_boot_complete_first_draw = True
		self.show_provision()
		self.navigate(LauncherApp(self))
	def show_provision(self):
		img = image.Image(resource.provision_image_path)
		# del img
		img.draw_string(50, 6,
						"<-", lcd.RED)
		img.draw_string(100, 6,
						"ENTER", lcd.RED)
		img.draw_string(172, 6,
						"->", lcd.RED)
		img.draw_string(172, lcd.height() - 24,
						"POWER", lcd.RED)
		img.draw_string(50, lcd.height() - 24,
						"RESET", lcd.WHITE)
		lcd.display(img)
		self.wait_event()
	def button_irq(self, gpio, optional_pin_num=None):
		print("button_irq start:", gpio, optional_pin_num)
		if self.is_handling_irq:
			print("is_handing_irq, ignore")
			return
		self.is_handing_irq = True
		value = gpio.value()
		state = "released" if value else "pressed"
		print("button_irq:", gpio, optional_pin_num, state)
		if self.home_button is gpio:
			self.on_home_button_changed(state)
		elif self.back_button is gpio:
			self.on_next_button_changed(state)
		elif self.back_button is gpio:
			self.on_back_button_changed(state)
		self.is_handing_irq = False
		print("button_irq end:", gpio, optional_pin_num, state)
	def init_fm(self):
		fm.register(Buttom_ENTER_IO, fm.fpioa.GPIOHS10)
		self.home_button = GPIO(GPIO.GPIOHS10, GPIO.IN, GPIO.PULL_UP)
		if self.home_button.value() == 0:
			sys.exit()
		fm.register(Buttom_BACK_IO, fm.fpioa.GPIOHS11)
		self.back_button = GPIO(GPIO.GPIOHS11, GPIO.IN, GPIO.PULL_UP)
		fm.register(Buttom_NEXT_IO, fm.fpioa.GPIOHS16)
		self.next_button = GPIO(GPIO.GPIOHS16, GPIO.IN, GPIO.PULL_UP)
		fm.register(LED_R_IO, fm.fpioa.GPIOHS13)
		self.led_r = GPIO(GPIO.GPIOHS13, GPIO.OUT)
		self.led_r.value(1)
		fm.register(LED_G_IO, fm.fpioa.GPIOHS12)
		self.led_g = GPIO(GPIO.GPIOHS12, GPIO.OUT)
		self.led_g.value(1)
		fm.register(LED_B_IO, fm.fpioa.GPIOHS14)
		self.led_b = GPIO(GPIO.GPIOHS14, GPIO.OUT)
		self.led_b.value(1)
	def invalidate_drawing(self):
		print("invalidate_drawing")
		self.is_drawing_dirty = True
	def run(self):
		try:
			self.run_inner()
		except Exception as e:
			import uio
			string_io = uio.StringIO()
			sys.print_exception(e, string_io)
			s = string_io.getvalue()
			lcd.clear(lcd.RED)
			msg = "** " + str(e)
			chunks, chunk_size = len(msg), 29
			msg_lines = [msg[i:i+chunk_size]
						 for i in range(0, chunks, chunk_size)]
			x_offset = 5
			lcd.draw_string(
				x_offset, 1, "A problem has been detected and windows", lcd.WHITE, lcd.RED)
			lcd.draw_string(
				x_offset, 1 + 5 + 16, "Technical information:", lcd.WHITE, lcd.RED)
			current_y = 1 + 5 + 16 * 2
			for line in msg_lines:
				lcd.draw_string(x_offset, current_y, line, lcd.WHITE, lcd.RED)
				current_y += 16
				if current_y >= lcd.height():
					break
			lcd.draw_string(x_offset, current_y, s, lcd.WHITE, lcd.RED)
			lcd.draw_string(x_offset, lcd.height() - 36, "-----------------------------", lcd.WHITE, lcd.RED)
			lcd.draw_string(
				x_offset, lcd.height() - 20, "Will reboot after 10 seconds..", lcd.WHITE, lcd.RED)
	def wait_event(self):
		"""key event or view invalidate event"""
		print("wait for all key release")
		while (self.home_button.value() == 0
			or self.back_button.value() == 0
			or self.next_button.value() == 0):
			pass
		print("key released, now wait for a event")
		while (self.home_button.value() == 1
				and self.back_button.value() == 1
				and self.next_button.value() == 1
				and not self.is_drawing_dirty):
			pass
		print("some event arrived")
		if self.is_drawing_dirty:
			print("EVENT: drawing dirty event")
			return ("drawing", "dirty")
		elif self.home_button.value() == 0:
			print("EVENT: home_button pressed")
			return (self.home_button, "pressed")
			self.on_home_button_changed("pressed")
		elif self.back_button.value() == 0:
			print("EVENT: back_button pressed")
			return (self.back_button, "pressed")
			self.on_back_button_changed("pressed")
		elif self.next_button.value() == 0:
			print("EVENT: next_button pressed")
			return (self.next_button, "pressed")
			self.on_next_button_changed("pressed")
		else:
			return None
	def run_inner(self):
		while True:
			print("---")
			if self.is_drawing_dirty:
				print("drawing is dirty")
				self.is_drawing_dirty = False
				current_app = self.get_current_app()
				print("System| before on_draw() of", current_app, "free memory:", gc.mem_free())
				print("System| current_app.on_draw() start")
				current_app.on_draw()
				print("System| current_app.on_draw() end")
				print("System| on_draw() of", current_app, "called, free memory:", gc.mem_free())
				print("System|after gc.collect(), free memory:", gc.mem_free())
				time.sleep_ms(1)
			else:
				event_info = self.wait_event()
				if event_info is not None and len(event_info) == 2:
					event = event_info[0]
					state = event_info[1]
					if event == self.home_button:
						self.on_home_button_changed(state)
					elif event == self.back_button:
						self.on_back_button_changed(state)
					elif event == self.next_button:
						self.on_next_button_changed(state)
	def navigate(self, app):
		print("navigate")
		self.app_stack.append(app)
		self.invalidate_drawing()
	def navigate_back(self):
		if len(self.app_stack) > 0:
			print("pop >>>>>>>>>>")
			self.app_stack.pop()
		self.invalidate_drawing()
	def get_current_app(self):
		return self.app_stack[-1] if len(self.app_stack) > 0 else None
	def on_pek_button_pressed(self, axp):
		print("on_pek_button_pressed", axp)
		handled = False
		current_app = self.get_current_app()
		if current_app:
			try:
				handled = current_app.on_back_pressed()
			except NeedRebootException:
				machine.reset()
		if not handled:
			print("on_back_pressed() not handled, exit current app")
			self.navigate_back()
	def system_periodic_task(self, axp):
		current = self.get_current_app()
		if current:
			current.app_periodic_task()
	def on_home_button_changed(self, state):
		print("system:on_home_button_changed", state)
		self.home_button_state = not self.home_button_state
		self.led_r.value(self.home_button_state)
		self.get_current_app().on_home_button_changed(state)
	def on_back_button_changed(self, state):
		print("system:on_back_button_changed", state)
		self.back_button_state = not self.back_button_state
		self.led_g.value(self.back_button_state)
		self.get_current_app().on_back_button_changed(state)
	def on_next_button_changed(self, state):
		print("system:on_next_button_changed", state)
		self.next_button_state = not self.next_button_state
		self.led_b.value(self.next_button_state)
		self.get_current_app().on_next_button_changed(state)
print('---------------')
class APP:
	def __init__(self):
		self.app = MaixCubeSystem()
		self.app.run()
	def getApp(self):
		return self.app
	def sayhello(self):
		print("Hello")
app_handle = APP()
app_handle.sayhello()
app = app_handle.getApp()
while True:
	time.sleep(100)
	print("Runing")
