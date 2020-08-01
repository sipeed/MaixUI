# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math, random, sensor, audio

from fpioa_manager import fm
from machine import I2C
from Maix import I2S, GPIO, FFT

from ui_catch import catch
from ui_canvas import ui
from ui_sample import sample_page
from core import agent
from wdt import protect

from led import cube_led
from button import cube_button
from pmu_axp173 import AXP173
from es8374 import ES8374
from msa301 import MSA301, _MSA301_I2CADDR_DEFAULT
from shtxx import SHT3x, SHT3x_ADDR, SHT31_ADDR
from bme280 import BME280, BME280_I2CADDR
from qmcx983 import QMCX983, QMCX983_I2CADDR

if __name__ == "__main__":

    class Report():

        Key_Test = False
        Led_Test = False
        Power_Test = False
        Audio_Test = False
        Sensor_Test = False
        Msa301_Test = False
        Grove_Test = False
        Spmod_Test = False

        def __init__(self):
            self.is_load = False

        def load(self):
            if self.is_load == False:
                #print(case.load)
                self.is_load = True

        def work(self):
            #print(case.work)
            y = 0
            ui.canvas.draw_string(20, y, "1 Key_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Key_Test), (0, 255, 0) if (Report.Key_Test) else (255, 0, 0), scale=2)
            y += 30
            ui.canvas.draw_string(20, y, "2 Led_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Led_Test), (0, 255, 0) if (Report.Led_Test) else (255, 0, 0), scale=2)
            y += 30
            ui.canvas.draw_string(20, y, "3 Power_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Power_Test), (0, 255, 0) if (Report.Power_Test) else (255, 0, 0), scale=2)
            y += 30
            ui.canvas.draw_string(20, y, "4 Audio_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Audio_Test), (0, 255, 0) if (Report.Audio_Test) else (255, 0, 0), scale=2)
            y += 30
            ui.canvas.draw_string(20, y, "5 Sensor_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Sensor_Test), (0, 255, 0) if (Report.Sensor_Test) else (255, 0, 0), scale=2)
            y += 30
            ui.canvas.draw_string(20, y, "6 Msa301_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Msa301_Test), (0, 255, 0) if (Report.Msa301_Test) else (255, 0, 0), scale=2)
            y += 30
            ui.canvas.draw_string(20, y, "7 Grove_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Grove_Test), (0, 255, 0) if (Report.Grove_Test) else (255, 0, 0), scale=2)
            y += 30
            ui.canvas.draw_string(20, y, "8 Spmod_Test", (127, 255, 255), scale=2)
            ui.canvas.draw_string(180, y, str(Report.Spmod_Test), (0, 255, 0) if (Report.Spmod_Test) else (255, 0, 0), scale=2)

        def free(self):
            if self.is_load:
                #print(sample.free)
                self.is_load = False

    class KeyTest():

        def __init__(self):
            self.is_load = False
            self.load()

        def load(self):
            if self.is_load == False:
                #print(case.load)
                self.is_load = True
                sample_page.btn.enable = False
                self.btn = cube_button()
                self.btn.config(10, 11, 16)
                self.agent = agent()
                self.agent.event(150, self.key_event)
                self.agent.event(5000, lambda :sample_page.next())
                self.home_click = 0
                self.back_click = 0
                self.next_click = 0

        def key_event(self):
            self.btn.expand_event()

            if self.btn.back() == 2:
                self.back_click += 1
            elif self.btn.next() == 2:
                self.next_click += 1
            elif self.btn.home() == 2:
                self.home_click += 1
                if self.btn.interval() > 2000: # long press
                    sample_page.next()
            if self.home_click > 0 and self.back_click > 0 and self.next_click > 0:
                Report.Key_Test = True
                sample_page.next()

        def work(self):
            self.agent.parallel_cycle()
            y = 40
            ui.canvas.draw_string(20, y,
                'home_click %d' % self.home_click, (255, 0, 0), scale=2)
            y += 40
            ui.canvas.draw_string(20, y,
                'back_click %d' % self.back_click, (0, 255, 0), scale=2)
            y += 40
            ui.canvas.draw_string(20, y,
                'next_click %d' % self.next_click, (0, 0, 255), scale=2)
            y += 40
            ui.canvas.draw_string(10, y,
                ' center (home) key \nPress 2s or Wait 3s \n  into next test', (255, 255, 255), scale=2)

        def free(self):
            if self.is_load:
                #print(sample.free)
                self.is_load = False
                sample_page.btn.enable = True
                if self.home_click > 0 and self.back_click > 0 and self.next_click > 0:
                    Report.Key_Test = True

    class LedTest():

        def __init__(self):
            self.is_load = False
            #self.load()

        def load(self):
            if self.is_load == False:
                #print(case.load)
                self.is_load = True
                sample_page.btn.enable = False
                self.btn = cube_button()
                self.btn.config(10, 11, 16)
                cube_led.init(13, 12, 14, 32)
                self.agent = agent()
                self.agent.event(150, self.key_event)
                self.agent.event(500, self.test_event)
                self.agent.event(5000, lambda :sample_page.next())
                self.r = 0
                self.g = 0
                self.b = 0
                self.w = 0
                self.state = 0

        def test_event(self):
            if self.state == 0:
                cube_led.w.value(1)
                cube_led.r.value(0)
            if self.state == 1:
                cube_led.r.value(1)
                cube_led.g.value(0)
            if self.state == 2:
                cube_led.g.value(1)
                cube_led.b.value(0)
            if self.state == 3:
                cube_led.b.value(1)
                cube_led.w.value(0)

        def key_event(self):
            self.btn.expand_event()

        def work(self):
            self.agent.parallel_cycle()

            y = 0
            ui.canvas.draw_string(20, y,
                'r %d' % self.r, (255, 0, 0), scale=2)
            y += 40
            ui.canvas.draw_string(20, y,
                'g %d' % self.g, (0, 255, 0), scale=2)
            y += 40
            ui.canvas.draw_string(20, y,
                'b %d' % self.b, (0, 0, 255), scale=2)
            y += 40
            ui.canvas.draw_string(20, y,
                'w %d' % self.w, (0, 0, 255), scale=2)
            y += 40
            ui.canvas.draw_string(10, y,
                'left-key is Pass\n        right-key is Fail \nWait 5s into next test', (255, 255, 255), scale=2)

            if self.btn.home() == 2:
                if self.btn.interval() > 2000: # long press
                    sample_page.next()

            elif self.btn.back() == 2:
                if self.state == 0:
                    cube_led.r.value(1)
                    self.r -= 1
                    self.state = 1
                elif self.state == 1:
                    cube_led.g.value(1)
                    self.g -= 1
                    self.state = 2
                elif self.state == 2:
                    cube_led.b.value(1)
                    self.b -= 1
                    self.state = 3
                elif self.state == 3:
                    cube_led.w.value(1)
                    self.w -= 1
                    self.state = 0

            elif self.btn.next() == 2:
                if self.state == 0:
                    cube_led.r.value(1)
                    self.r += 1
                    self.state = 1
                elif self.state == 1:
                    cube_led.g.value(1)
                    self.g += 1
                    self.state = 2
                elif self.state == 2:
                    cube_led.b.value(1)
                    self.b += 1
                    self.state = 3
                elif self.state == 3:
                    cube_led.w.value(1)
                    self.w += 1
                    self.state = 0

            elif self.r > 0 and self.g > 0 and self.b > 0 and self.w > 0:
                Report.Led_Test = True
                sample_page.next()

        def free(self):
            if self.is_load:
                #print(sample.free)
                self.is_load = False
                cube_led.r.value(1)
                cube_led.g.value(1)
                cube_led.b.value(1)
                cube_led.w.value(1)
                sample_page.btn.enable = True
                if self.r > 0 and self.g > 0 and self.b > 0 and self.w > 0:
                    Report.Led_Test = True

    class PowerTest():

        def __init__(self):
            self.is_load = False
            self.i2c = I2C(I2C.I2C1, freq=100*1000, scl=30, sda=31)
            #fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
            #fm.register(31, fm.fpioa.I2C1_SDA, force=True)
        def test_event(self):
            if self.isconnected and self.vbat_voltage > 0 and self.usb_voltage:
                Report.Power_Test = True

            sample_page.next()

        def load(self):
            if self.is_load == False:
                # i2c init()
                sample_page.btn.enable = False
                fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
                fm.register(31, fm.fpioa.I2C1_SDA, force=True)
                self.isconnected = False
                self.isError = None
                self.work_info = []
                self.agent = agent()
                self.agent.event(500, self.check)
                self.agent.event(3000, self.test_event)
                self.is_load = True

        def free(self):
            if self.is_load:
                # i2c deinit()
                sample_page.btn.enable = True
                self.is_load = False

        def check(self):
            try:
                if self.isconnected == False:
                    if _MSA301_I2CADDR_DEFAULT in self.i2c.scan():
                        self.axp173 = AXP173(self.i2c)
                        self.isconnected = True
                        self.axp173.enable_adc(True)
                        # 默认充电限制在 4.2V, 190mA 档位
                        self.axp173.setEnterChargingControl(True)
                        self.axp173.exten_output_enable()
                else:
                    tmp = []
                    self.work_mode = self.axp173.getPowerWorkMode()
                    tmp.append("WorkMode:" + hex(self.work_mode))

                    # 检测 电池电压
                    self.vbat_voltage = self.axp173.getVbatVoltage()
                    tmp.append("vbat_voltage: {0} V".format(self.vbat_voltage))

                    # 检测 电池充电电流
                    self.BatteryChargeCurrent = self.axp173.getBatteryChargeCurrent()
                    tmp.append("BatChargeCurrent: {0:>4.1f}mA".format(
                        self.BatteryChargeCurrent))

                    # 检测 USB-ACIN 电压
                    self.usb_voltage = self.axp173.getUSBVoltage()
                    tmp.append("usb_voltage: {0:>4}mV".format(self.usb_voltage))

                    # 检测 USB-ACIN 电流
                    self.USBInputCurrent = self.axp173.getUSBInputCurrent()
                    tmp.append("USBInputCurrent: {0:>4.1f}mA".format(self.USBInputCurrent))

                    ### 检测 VBUS 电压
                    #usb_voltage = self.axp173.getConnextVoltage()
                    #print("6 VUBS_voltage: " + str(usb_voltage))

                    ### 检测 VBUS 电流
                    #USBInputCurrent = self.axp173.getConnextInputCurrent()
                    #print("7 VUBSInputCurrent: " + str(USBInputCurrent) + "mA")

                    self.getChargingControl = self.axp173.getChargingControl()
                    tmp.append("ChargingControl: {}".format(hex(self.getChargingControl)))

                    # 检测 是否正在充电
                    if self.axp173.is_charging() == True:
                        tmp.append("Charging....")
                    else:
                        tmp.append("Not Charging")
                    tmp.append(self.axp173.is_charging())

                    # 检测 USB 是否连接
                    if self.axp173.is_usb_plugged_in() == 1:
                        tmp.append("USB plugged ....")
                    else:
                        tmp.append("USB is not plugged in")

                    self.work_info = tmp
            except Exception as e:
                Report.Power_Test = False
                Report.isError = str(e)
                print(e)

        def work(self):
            self.agent.parallel_cycle()

            ui.canvas.draw_string(30, 10, "Power Test", (127, 127, 255), scale=2)
            ui.canvas.draw_string(30, 40, "isconnected: %s" % (
                str)(self.isconnected), (255, 127, 0), scale=1)
            if self.isconnected:
                for i in range(len(self.work_info)):
                    ui.canvas.draw_string(
                        20, 20*i + 60, "{0}".format(str(self.work_info[i])), mono_space=1)
            if self.isError != None:
                ui.canvas.draw_string(40, 60, self.isError, (255, 255, 255), scale=2)
                sample_page.next()

    class GroveTest():

        def __init__(self, scl=30, sda=31):
            self.is_load = False
            self.scl = scl
            self.sda = sda
            self.i2c = I2C(I2C.I2C1, freq=100*1000, scl=self.scl, sda=self.sda)
            #fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
            #fm.register(31, fm.fpioa.I2C1_SDA, force=True)

        def test_event(self):
            if self.isconnected and self.work_data != None and self.work_data[0] > 0 and self.work_data[1] > 1:
                Report.Grove_Test = True
            sample_page.next()

        def load(self):
            if self.is_load == False:
                # i2c init()
                sample_page.btn.enable = False
                fm.register(self.scl, fm.fpioa.I2C1_SCLK, force=True)
                fm.register(self.sda, fm.fpioa.I2C1_SDA, force=True)
                self.isconnected = False
                self.isError = None
                self.work_info = []
                self.work_data = None
                self.agent = agent()
                self.agent.event(500, self.check)
                self.agent.event(3000, self.test_event)
                self.is_load = True

        def free(self):
            if self.is_load:
                # i2c deinit()
                sample_page.btn.enable = True
                self.is_load = False

        def check(self):
            try:
                if self.isconnected == False:
                    if SHT3x_ADDR in self.i2c.scan():
                        self.sht3x = SHT3x(self.i2c, SHT3x_ADDR)
                        self.isconnected = True
                    if SHT31_ADDR in self.i2c.scan():
                        self.sht3x = SHT3x(self.i2c, SHT31_ADDR)
                        self.isconnected = True
                else:
                    tmp = []
                    self.work_data = self.sht3x.read_temp_humd()
                    tmp.append("data:" + str(self.work_data))
                    self.work_info = tmp
            except Exception as e:
                Report.Grove_Test = False
                Report.isError = str(e)
                print(e)

        def work(self):
            self.agent.parallel_cycle()

            ui.canvas.draw_string(30, 10, "Grove Test SHT3X", (0, 255, 127), scale=2)
            ui.canvas.draw_string(30, 40, "isconnected: %s" % (
                str)(self.isconnected), (255, 127, 0), scale=2)
            if self.isconnected:
                for i in range(len(self.work_info)):
                    ui.canvas.draw_string(
                        20, 20*i + 60, "{0}".format(str(self.work_info[i])), mono_space=1)
            if self.isError != None:
                ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
                sample_page.next()

    class SpmodTest():

        def __init__(self, scl=6, sda=7):
            self.is_load = False
            self.scl = scl
            self.sda = sda
            self.i2c = I2C(I2C.I2C1, freq=100*1000, scl=self.scl, sda=self.sda)
            #fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
            #fm.register(31, fm.fpioa.I2C1_SDA, force=True)

        def test_event(self):
            if self.isconnected and self.config_bme and self.config_qmcx and self.cache_bme[0] != 0  and self.config_qmcx[0] != 0:
                Report.Spmod_Test = True
            sample_page.next()

        def load(self):
            if self.is_load == False:
                # i2c init()
                sample_page.btn.enable = False
                fm.register(self.scl, fm.fpioa.I2C1_SCLK, force=True)
                fm.register(self.sda, fm.fpioa.I2C1_SDA, force=True)
                self.isconnected = False
                self.isError = None
                self.config_bme = False
                self.config_qmcx = False
                self.cache_bme = (0, 0, 0)
                self.cache_qmcx = (0, 0, 0)
                self.agent = agent()
                self.agent.event(500, self.check)
                self.agent.event(3000, self.test_event)
                self.is_load = True

        def free(self):
            if self.is_load:
                # i2c deinit()
                sample_page.btn.enable = True
                self.is_load = False

        def check(self):
            try:
                if self.isconnected == False:
                    if self.config_bme == False:
                        if BME280_I2CADDR in self.i2c.scan():
                            self.bme = BME280(i2c=self.i2c)
                            self.config_bme = True
                    if self.config_qmcx == False:
                        if QMCX983_I2CADDR in self.i2c.scan():
                            self.qmcx = QMCX983(i2c=self.i2c)
                            self.config_qmcx = True
                else:
                    if self.config_bme:
                        self.cache_bme = self.bme.read_compensated_data()
                    if self.config_qmcx:
                        self.cache_qmcx = self.qmcx.read_xyz()
            except Exception as e:
                Report.Spmod_Test = False
                Report.isError = str(e)
                print(e)

        def bmevalues(self, data):
            t, p, h = data

            p = p // 256
            pi = p // 100
            pd = p - pi * 100
            p = pi + (pd / 100)

            hi = h // 1024
            hd = h * 100 // 1024 - hi * 100
            h = hi + (hd / 100)
            return "T{:.1f} C, P{:.2f} hPa, H{:.2f}%".format(t/100, p, h)
            #return "[] T={:.1f}\xb0C, P={:.2f}hPa, H={:.2f}%".format(t/100, p, h)

        def work(self):
            self.agent.parallel_cycle()

            ui.canvas.draw_string(10, 10, "Spmod Test", (127, 255, 0), scale=3)
            ui.canvas.draw_string(30, 50, "BME280: %s" % (
                str)(self.config_bme), (255, 127, 0), scale=2)
            ui.canvas.draw_string(30, 70, "QMCX983: %s" % (
                str)(self.config_qmcx), (255, 127, 0), scale=2)
            if self.config_bme:
                ui.canvas.draw_string(20, 100,
                    self.bmevalues(self.cache_bme), (127, 255, 255), scale=1)
            if self.config_qmcx:
                x, y, z = self.cache_qmcx
                ui.canvas.draw_string(20, 200, "({:0<3d}, {:0<3d}, {:0<3d})".format(int(x), int(y), int(z)), color=(127, 255, 255), scale=2)
                ui.canvas.draw_string(10, 130, "x", (255, 127, 0), scale=2)
                ui.canvas.draw_line(30, 140, int((x / 5) + 20), 140, color=(41, 131, 255))
                ui.canvas.draw_string(10, 150, "y", (255, 127, 0), scale=2)
                ui.canvas.draw_line(30, 160, int((y / 5) + 20), 160, color=(141, 31, 255))
                ui.canvas.draw_string(10, 170, "z", (255, 127, 0), scale=2)
                ui.canvas.draw_line(30, 180, int((z / 5) + 20), 180, color=(241, 131, 55))
            if self.isError != None:
                ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
                sample_page.next()

    class Msa301Test():

        def __init__(self, scl=30, sda=31):
            self.is_load = False
            self.scl = scl
            self.sda = sda
            self.i2c = I2C(I2C.I2C1, freq=100*1000, scl=self.scl, sda=self.sda)
            #fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
            #fm.register(31, fm.fpioa.I2C1_SDA, force=True)

        def test_event(self):
            if self.isconnected and self.acceleration[0] != 0 and self.acceleration[1] != 0 and self.acceleration[2] != 0:
                Report.Msa301_Test = True
            sample_page.next()

        def load(self):
            if self.is_load == False:
                # i2c init()
                sample_page.btn.enable = False
                fm.register(self.scl, fm.fpioa.I2C1_SCLK, force=True)
                fm.register(self.sda, fm.fpioa.I2C1_SDA, force=True)
                self.isconnected = False
                self.isError = None
                self.tapped = False
                self.acceleration = (0, 0, 0)
                self.agent = agent()
                self.agent.event(500, self.check)
                self.agent.event(3000, self.test_event)
                self.is_load = True

        def free(self):
            if self.is_load:
                # i2c deinit()
                sample_page.btn.enable = True
                self.is_load = False

        def check(self):
            try:
                if self.isconnected == False:
                    if _MSA301_I2CADDR_DEFAULT in self.i2c.scan():
                        self.msa301 = MSA301(self.i2c)
                        self.isconnected = True
                else:
                    self.tapped = self.msa301.tapped
                    self.acceleration = self.msa301.acceleration
            except Exception as e:
                Report.Msa301_Test = False
                Report.isError = str(e)
                print(e)

        def work(self):
            self.agent.parallel_cycle()

            ui.canvas.draw_string(30, 30, "MSA301 Test", (127, 127, 255), scale=3)
            ui.canvas.draw_string(30, 80, "isconnected: %s" % (
                str)(self.isconnected), (255, 127, 0), scale=2)
            if self.isconnected:
                ui.canvas.draw_string(30, 120, "tapped: %s" % (
                    str)(self.tapped), (0, 214, 126), scale=2)

                ui.canvas.draw_string(10, 140, "x", (255, 0, 0), scale=2)
                ui.canvas.draw_line(120, 150, 120 + int(self.acceleration[0] * 8), 150, color=(41, 131, 255))
                ui.canvas.draw_string(10, 160, "y", (0, 255, 0), scale=2)
                ui.canvas.draw_line(120, 170, 120 + int(self.acceleration[1] * 8), 170, color=(141, 31, 255))
                ui.canvas.draw_string(10, 180, "z", (0, 0, 255), scale=2)
                ui.canvas.draw_line(120, 190, 120 + int(self.acceleration[2] * 8), 190, color=(241, 131, 55))

                ui.canvas.draw_string(40, 210,
                    str(("%-02.2f %-02.2f %-02.2f" % self.acceleration)), (127, 255, 255), scale=2)

            if self.isError != None:
                ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
                sample_page.next()

    class SensorTest():

        def __init__(self):
            self.is_load = False

        def test_event(self):
            if self.get_image != None:
                Report.Sensor_Test = True
            sample_page.next()

        def check(self):
            try:
                if self.isconnected == False:
                    try:
                        sensor.reset(dual_buff=True)
                        sensor.set_pixformat(sensor.YUV422)
                        sensor.set_framesize(sensor.QVGA)
                        sensor.set_hmirror(1)
                        sensor.set_vflip(1)
                        sensor.run(1)
                        sensor.skip_frames()
                        self.isconnected = True
                    except Exception as e:
                        Report.Msa301_Test = False
                        Report.isError = str(e)
                        print(e)
            except Exception as e:
                Report.Msa301_Test = False
                Report.isError = str(e)
                print(e)

        def load(self):
            if self.is_load == False:
                sample_page.btn.enable = False
                self.get_image = None
                self.isError = None
                self.isconnected = False
                self.agent = agent()
                self.agent.event(100, self.check)
                self.agent.event(4000, self.test_event)
                self.is_load = True

        def free(self):
            if self.is_load:
                sample_page.btn.enable = True
                self.is_load = False

        def work(self):
            self.agent.parallel_cycle()
            if self.isconnected:
                try:
                    self.get_image = sensor.snapshot()
                    ui.canvas.draw_image(self.get_image, 0, 0)
                    ui.canvas.draw_string(30, 30, "Sensor Test", (127, 127, 255), scale=3)
                    ui.canvas.draw_string(30, 70, "isconnected: %s" % (
                        str)(self.isconnected), (255, 127, 0), scale=2)
                except Exception as e:
                    print(e)
            if self.isError != None:
                ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
                sample_page.next()

    class AudioTest():

        def __init__(self, scl=30, sda=31):
            self.is_load = False
            self.scl = scl
            self.sda = sda
            #self.load()
            self.i2c = I2C(I2C.I2C1, freq=100*1000, scl=self.scl, sda=self.sda)

        def key_event(self):
            self.btn.expand_event()

            if self.btn.back() == 2:
                self.result -= 1
                self.state += 1
            elif self.btn.next() == 2:
                self.result += 1
                self.state += 1

        def test_event(self):
            if self.isconnected and self.result == 2:
                self.result = 0
                Report.Audio_Test = True
            sample_page.next()

        def load(self):
            if self.is_load == False:
                # i2c init()
                sample_page.btn.enable = False
                #fm.register(30, fm.fpioa.I2C1_SCLK, force=True)
                #fm.register(31, fm.fpioa.I2C1_SDA, force=True)
                self.isconnected = False
                self.isError = None
                self.is_play = False
                self.is_record = False
                self.state = 0
                self.result = 0
                self.fft_amp = None
                self.btn = cube_button()
                self.btn.config(10, 11, 16)
                self.agent = agent()
                self.agent.event(150, self.key_event)
                self.agent.event(500, self.check)
                self.agent.event(6000, self.test_event)
                fm.register(19,fm.fpioa.I2S0_MCLK, force=True)
                fm.register(35,fm.fpioa.I2S0_SCLK, force=True)
                fm.register(33,fm.fpioa.I2S0_WS, force=True)
                fm.register(34,fm.fpioa.I2S0_IN_D0, force=True)
                fm.register(18,fm.fpioa.I2S0_OUT_D2, force=True)
                fm.register(self.scl, fm.fpioa.I2C1_SCLK, force=True)
                fm.register(self.sda, fm.fpioa.I2C1_SDA, force=True)
                self.is_load = True

        def free(self):
            if self.is_load:
                # i2c deinit()
                sample_page.btn.enable = True
                self.is_load = False

        def check(self):
            try:
                if self.isconnected == False:
                    if ES8374._ES8374_I2CADDR_DEFAULT in self.i2c.scan():
                        self.isconnected = True
                else:
                    if self.state == 0 and self.is_play == False:
                        self.is_play = True
                        self.es8374 = ES8374(self.i2c)
                        self.i2s = I2S(I2S.DEVICE_0, pll2=262144000, mclk=31)
                        self.i2s.channel_config(I2S.CHANNEL_2, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT, cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)
                        # init audio
                        self.player = audio.Audio(path="/flash/one.wav")
                        self.player.volume(80)
                        # read audio info
                        wav_info = self.player.play_process(self.i2s)
                        print("wav file head information: ", wav_info)
                        self.i2s.set_sample_rate(wav_info[1])
                        print('loop to play audio')

                    elif self.state == 1 and self.is_record == False:
                        self.is_record = True
                        self.es8374 = ES8374(self.i2c)
                        self.i2s = I2S(I2S.DEVICE_0, pll2=262144000, mclk=31)
                        self.i2s.channel_config(I2S.CHANNEL_0, I2S.RECEIVER, resolution=I2S.RESOLUTION_16_BIT, cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.STANDARD_MODE)
                        self.i2s.set_sample_rate(22050)

            except Exception as e:
                Report.Audio_Test = False
                Report.isError = str(e)
                print(e)

        def work(self):
            self.agent.parallel_cycle()

            ui.canvas.draw_string(30, 30, "Audio Test", (127, 127, 255), scale=3)
            ui.canvas.draw_string(30, 70, "isconnected: %s" % (
                str)(self.isconnected), (255, 127, 0), scale=2)

            ui.canvas.draw_string(30, 100, "Left-Key is Fail\nRight-Key is Pass\n", (127, 127, 255), scale=2)

            ui.canvas.draw_string(30, 150, "state: %s" %
                ('Test play' if self.state == 0 else 'Test record'), (255, 127, 0), scale=2)

            if self.isconnected:
                if self.state == 0 and self.is_play:
                    ret = self.player.play()
                    if ret == None or ret == 0:
                        self.player.finish()
                        # init audio
                        self.player = audio.Audio(path="/flash/one.wav")
                        self.player.volume(80)
                        # read audio info
                        wav_info = self.player.play_process(self.i2s)
                        self.i2s.set_sample_rate(wav_info[1])
                elif self.state == 1 and self.is_record:
                    tmp = self.i2s.record(1024)
                    fft_res = FFT.run(tmp.to_bytes(), 512)
                    fft_amp = FFT.amplitude(fft_res)
                    if fft_amp[50] > 100 and fft_amp[100] > 100:
                        Report.Audio_Test = True
                        sample_page.next()
                    for x_shift in range(240):
                        hist_height = fft_amp[x_shift]
                        ui.canvas.draw_rectangle((x_shift, 0, 1, hist_height), [255,255,255], 1, True)
                        #print((x_shift, 0, 1, hist_height))
            if self.isError != None:
                ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
                sample_page.next()

    #Key_Test = False
    #Led_Test = False
    #Power_Test = False
    #Audio_Test = False
    #Sensor_Test = False
    #Msa301_Test = False
    #Grove_Test = False
    #Spmod_Test = False

    sample_page.add_sample(Report())
    sample_page.add_sample(SpmodTest())
    sample_page.add_sample(GroveTest())
    sample_page.add_sample(Msa301Test())
    sample_page.add_sample(SensorTest())
    sample_page.add_sample(AudioTest())
    sample_page.add_sample(PowerTest())
    sample_page.add_sample(LedTest())
    sample_page.add_sample(KeyTest())

    @ui.warp_template(ui.blank_draw)
    @ui.warp_template(sample_page.sample_draw)
    @catch
    def app_main():
        ui.display()

    import time, gc
    gc.collect()
    last = time.ticks_ms()
    while True:
        #app_main()
        #import time
        #last = time.ticks_ms()
        while True:
            # app_main()
            # protect.keep()
            try:
                #print((int)(1000 / (time.ticks_ms() - last)), 'fps')
                #last = time.ticks_ms()
                app_main()
                protect.keep()
                #time.sleep(0.1)
            except KeyboardInterrupt:
                protect.stop()
                raise KeyboardInterrupt()
            except Exception as e:
                print(e)
