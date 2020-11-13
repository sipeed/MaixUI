# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, gc, math, random, sensor, audio

from fpioa_manager import fm
from machine import I2C, SPI
from Maix import I2S, GPIO, FFT

from led import sipeed_led
from button import sipeed_button, button_io
from pmu_axp173 import AXP173, AXP173_ADDR
from sound import CubeAudio
from msa301 import MSA301, _MSA301_I2CADDR_DEFAULT
from shtxx import SHT3x, SHT3x_ADDR, SHT31_ADDR
from bme280 import BME280, BME280_I2CADDR
from qmcx983 import QMCX983, QMCX983_I2CADDR

from ui_catch import catch
from ui_canvas import ui
from ui_sample import sample_page
from core import agent
from wdt import protect

protect.keep()

class Report():

    Key_Test = False
    Led_Test = False
    Touch_Test = False
    Power_Test = False
    Audio_Test = False
    FrontSensor_Test = False
    RearSensor_Test = False
    Msa301_Test = False
    Grove_Test = False
    Spmod_Test = False

    def __init__(self):
        self.is_load = False

    def load(self):
        if self.is_load == False:
            #print(case.load)
            self.is_load = True
            sample_page.btn.enable = False
            self.btn = sipeed_button()
            self.agent = agent()
            self.agent.event(150, self.key_event)

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            sample_page.back()
        elif self.btn.next() == 2:
            sample_page.next()
        elif self.btn.home() == 2:
            axp173 = AXP173(I2C(I2C.I2C4, freq=100*1000, scl=30, sda=31))
            axp173.__write_reg(0x32, 0x80) # turn off

    def work(self):
        self.agent.parallel_cycle()
        #print(case.work)
        y = 0
        ui.canvas.draw_string(100, y, "Power", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "1  " + str(Report.Power_Test), (0, 255, 0) if (Report.Power_Test) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30
        ui.canvas.draw_string(100, y, "Msa301", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "2  " + str(Report.Msa301_Test), (0, 255, 0) if (Report.Msa301_Test) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30
        ui.canvas.draw_string(100, y, "Grove", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "3  " + str(Report.Grove_Test), (0, 255, 0) if (Report.Grove_Test) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30
        ui.canvas.draw_string(100, y, "Spmod", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "4  " + str(Report.Spmod_Test), (0, 255, 0) if (Report.Spmod_Test) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30
        ui.canvas.draw_string(100, y, "Key + RGB", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "5  " + str(Report.Key_Test), (0, 255, 0) if (Report.Key_Test) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30
        ui.canvas.draw_string(100, y, "RearSensor", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "8  " + str(Report.RearSensor_Test), (0, 255, 0) if (Report.RearSensor_Test) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30
        ui.canvas.draw_string(100, y, "Audio", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "9  " + str(Report.Audio_Test), (0, 255, 0) if (Report.Audio_Test) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30
        ui.canvas.draw_string(100, y, "SdCard & Lcd", (127, 255, 255), scale=2)
        ui.canvas.draw_string(10, y, "*  " + str(True), (0, 255, 0) if (True) else (255, 0, 0), scale=2)
        ui.canvas.draw_line(10, y + 25, 240, y + 25, color=(255, 255, 255))
        y += 30

    def free(self):
        if self.is_load:
            #print(sample.free)
            self.is_load = False
            sample_page.btn.enable = True

class PowerTest():

    def __init__(self):
        self.is_load = False
        self.i2c = I2C(I2C.I2C4, freq=100*1000, scl=24, sda=27)
        #self.load()

    def test_event(self):
        if self.isconnected and self.vbat_voltage > 0 and self.usb_voltage:
            Report.Power_Test = True
        if Report.Power_Test:
            sample_page.next()

    def load(self):
        if Report.Power_Test:
            sample_page.next()
        if self.is_load == False:
            # i2c init()
            sample_page.btn.enable = False
            self.isconnected = False
            self.isError = None
            self.vbat_voltage = 0
            self.work_info = []
            self.agent = agent()
            self.agent.event(500, self.check)
            self.agent.event(1500, self.test_event)
            self.is_load = True

    def free(self):
        if self.is_load:
            # i2c deinit()
            sample_page.btn.enable = True
            self.is_load = False

    def check(self):
        try:
            if self.isconnected == False:
                if AXP173_ADDR in self.i2c.scan():
                    self.axp173 = AXP173(self.i2c)
                    self.isconnected = True
                    self.axp173.enable_adc(True)
                    # 默认充电限制在 4.2V, 190mA 档位
                    self.axp173.setEnterChargingControl(True)
                    self.axp173.exten_output_enable()
                    # amigo sensor config.
                    self.axp173.writeREG(0x27, 0x20)
                    self.axp173.writeREG(0x28, 0x0C)
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

        ui.canvas.draw_string(10, 10, "1 Power Test", (127, 127, 255), scale=3)
        ui.canvas.draw_string(10, 50, "isconnected: %s" % (
            str)(self.isconnected), (255, 127, 0), scale=2)
        if self.isconnected:
            for i in range(len(self.work_info)):
                ui.canvas.draw_string(
                    20, 20*i + 80, "{0}".format(str(self.work_info[i])), mono_space=2)
        if self.isError != None:
            ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
            sample_page.next()

class PowerReport():

    def __init__(self):
        self.is_load = False

    def load(self):
        if self.is_load == False:
            self.is_load = True
            self.agent = agent()
            self.agent.event(500, sample_page.next)
        else:
            sample_page.next()

    def work(self):
        self.agent.cycle()
        ui.canvas.draw_string(10, 20, "1 PowerReport", (127, 255, 255), scale=3)
        ui.canvas.draw_string(30, 120, "Pass" if (Report.Power_Test) else "Fail", (0, 255, 0) if (Report.Power_Test) else (255, 0, 0), scale=8)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False

class Msa301Test():

    def __init__(self):
        self.is_load = False
        self.i2c = I2C(I2C.I2C4, freq=100*1000, scl=24, sda=27)

    def test_event(self):
        if self.isconnected and self.acceleration[0] != 0 and self.acceleration[1] != 0 and self.acceleration[2] != 0:
            Report.Msa301_Test = True
        sample_page.next()

    def load(self):
        if Report.Msa301_Test:
            sample_page.next()
        if self.is_load == False:
            # i2c init()
            sample_page.btn.enable = False
            self.isconnected = False
            self.isError = None
            self.tapped = False
            self.acceleration = (0, 0, 0)
            self.agent = agent()
            self.agent.event(500, self.check)
            self.agent.event(1500, self.test_event)
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

        ui.canvas.draw_string(10, 30, "2 Msa301Test", (127, 127, 255), scale=3)
        ui.canvas.draw_string(10, 80, "isconnected: %s" % (
            str)(self.isconnected), (255, 127, 0), scale=2)
        if self.isconnected:
            ui.canvas.draw_string(10, 120, "tapped: %s" % (
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

class Msa301Report():

    def __init__(self):
        self.is_load = False

    def load(self):
        if self.is_load == False:
            self.is_load = True
            self.agent = agent()
            self.agent.event(500, sample_page.next)
        else:
            sample_page.next()

    def work(self):
        self.agent.cycle()
        ui.canvas.draw_string(10, 20, "2 Msa301Report", (127, 255, 255), scale=3)
        ui.canvas.draw_string(30, 120, "Pass" if (Report.Msa301_Test) else "Fail", (0, 255, 0) if (Report.Msa301_Test) else (255, 0, 0), scale=8)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False

class GroveTest():

    def __init__(self):
        self.is_load = False
        self.i2c = I2C(I2C.I2C4, freq=100*1000, scl=9, sda=7)

    def test_event(self):
        if self.isconnected and self.work_data != None and self.work_data[0] > 0 and self.work_data[1] > 1:
            Report.Grove_Test = True
        sample_page.next()

    def load(self):
        if Report.Grove_Test:
            sample_page.next()
        if self.is_load == False:
            # i2c init()
            sample_page.btn.enable = False
            self.isconnected = False
            self.isError = None
            self.work_info = []
            self.work_data = None
            self.agent = agent()
            self.agent.event(250, self.check)
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
                # print(self.i2c.scan())
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

        ui.canvas.draw_string(10, 10, "3 Grove Test SHT3X", (0, 255, 127), scale=2)
        ui.canvas.draw_string(10, 50, "isconnected: %s" % (
            str)(self.isconnected), (255, 127, 0), scale=2)
        if self.isconnected:
            for i in range(len(self.work_info)):
                ui.canvas.draw_string(
                    20, 20*i + 90, "{0}".format(str(self.work_info[i])), scale=2)
        if self.isError != None:
            ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
            sample_page.next()

class GroveReport():

    def __init__(self):
        self.is_load = False

    def load(self):
        if self.is_load == False:
            self.is_load = True
            self.agent = agent()
            self.agent.event(500, sample_page.next)
        else:
            sample_page.next()

    def work(self):
        self.agent.cycle()
        ui.canvas.draw_string(10, 20, "3 GroveReport", (127, 255, 255), scale=3)
        ui.canvas.draw_string(30, 120, "Pass" if (Report.Grove_Test) else "Fail", (0, 255, 0) if (Report.Grove_Test) else (255, 0, 0), scale=8)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False

class SpmodTest():

    test_conut = 0

    def __init__(self, mosi=8, miso=15, cs=20, clk=21):
        self.is_load = False
        self.spi = SPI(SPI.SPI_SOFT, mode=SPI.MODE_MASTER, baudrate=400*1000,
            polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=clk, mosi=mosi, miso=miso)
        fm.register(cs, fm.fpioa.GPIO6, force=True)
        self.cs = GPIO(GPIO.GPIO6, GPIO.OUT)

    def test_event(self):
        if self.work_data != None and self.work_data == b'\x0b\x17':
            Report.Spmod_Test = True
        sample_page.next()

    def load(self):
        if Report.Spmod_Test:
            sample_page.next()
        if self.is_load == False:
            # i2c init()
            sample_page.btn.enable = False
            self.isError = None
            self.work_info = []
            self.work_data = None
            self.agent = agent()
            self.agent.event(250, self.check)
            self.agent.event(1500, self.test_event)
            self.is_load = True

    def free(self):
        if self.is_load:
            # i2c deinit()
            sample_page.btn.enable = True
            self.is_load = False

    def check(self):
        try:
            tmp = []
            self.cs.value(0)
            write_data = bytearray([0x90, 0x00, 0x00, 0x00])
            self.spi.write(write_data)
            id_buf = bytearray(2)
            self.spi.readinto(id_buf, write=0xff)
            self.work_data = id_buf
            self.cs.value(1)
            tmp.append("Flash ReadID\n\n" + str(self.work_data))
            self.work_info = tmp
        except Exception as e:
            Report.Spmod_Test = False
            Report.isError = str(e)
            print(e)

    def work(self):
        self.agent.parallel_cycle()

        ui.canvas.draw_string(10, 10, "4 Spmod Test", (0, 255, 127), scale=2)
        if self.work_data:
            for i in range(len(self.work_info)):
                ui.canvas.draw_string(
                    20, 20*i + 90, "{0}".format(str(self.work_info[i])), scale=2)
        if self.isError != None:
            ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
            sample_page.next()

class SpmodReport():

    def __init__(self):
        self.is_load = False

    def load(self):
        if self.is_load == False:
            self.is_load = True
            self.agent = agent()
            self.agent.event(500, sample_page.next)
        else:
            sample_page.next()

    def work(self):
        self.agent.cycle()
        ui.canvas.draw_string(10, 20, "4 SpmodReport", (127, 255, 255), scale=3)
        ui.canvas.draw_string(30, 120, "Pass" if (Report.Spmod_Test) else "Fail", (0, 255, 0) if (Report.Spmod_Test) else (255, 0, 0), scale=8)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False

class WaitTestStart():

    def __init__(self):
        self.is_load = False

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            sample_page.next()
        elif self.btn.next() == 2:
            sample_page.next()
        elif self.btn.home() == 2:
            sample_page.next()

    def load(self):
        if self.is_load == False:
            self.is_load = True
            sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.agent = agent()
            self.agent.event(150, self.key_event)
            #self.agent.event(500, sample_page.next)
        else:
            if Report.Key_Test:
                sample_page.next()

    def work(self):
        self.agent.cycle()
        ui.canvas.draw_string(10, 20, "Press \n\n Any-key \n\n Start Test", (127, 255, 255), scale=3)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False
        sample_page.btn.enable = True

class KeyTest():

    home_click = 0
    back_click = 0
    next_click = 0

    def __init__(self):
        self.is_load = False
        #self.load()

    def load(self):
        if Report.Key_Test:
            sample_page.next()
        if self.is_load == False:
            #print(case.load)
            self.is_load = True
            sample_page.btn.enable = False
            sipeed_led.init(14, 15, 17, 32)
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.agent = agent()
            self.agent.event(150, self.key_event)
            self.agent.event(16000, lambda :sample_page.next())
            KeyTest.home_click = 0
            KeyTest.back_click = 0
            KeyTest.next_click = 0

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            KeyTest.back_click += 1
            sipeed_led.r.value(0)
            sipeed_led.g.value(1)
            sipeed_led.b.value(1)
        elif self.btn.next() == 2:
            KeyTest.next_click += 1
            sipeed_led.r.value(1)
            sipeed_led.g.value(1)
            sipeed_led.b.value(0)
        elif self.btn.home() == 2:
            KeyTest.home_click += 1
            sipeed_led.r.value(1)
            sipeed_led.g.value(0)
            sipeed_led.b.value(1)
            if self.btn.interval() > 1500: # long press
                sample_page.next()
        if KeyTest.home_click > 1 and KeyTest.back_click > 1 and KeyTest.next_click > 1:
            Report.Key_Test = True
            sample_page.next()

    def work(self):
        self.agent.parallel_cycle()
        y = 20
        ui.canvas.draw_string(10, y,
            '5 KeyTest', (255, 255, 255), scale=3)
        y += 60
        ui.canvas.draw_string(20, y,
            'home click %d' % self.home_click, (255, 0, 0), scale=3)
        y += 60
        ui.canvas.draw_string(20, y,
            'back click %d' % self.back_click, (0, 255, 0), scale=3)
        y += 60
        ui.canvas.draw_string(20, y,
            'next click %d' % self.next_click, (0, 0, 255), scale=3)

    def free(self):
        if self.is_load:
            #print(sample.free)
            self.is_load = False
            sample_page.btn.enable = True
            if self.home_click > 0 and self.back_click > 0 and self.next_click > 0:
                Report.Key_Test = True
            sipeed_led.r.value(1)
            sipeed_led.g.value(1)
            sipeed_led.b.value(1)

class KeyReport():

    def __init__(self):
        self.is_load = False

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            sample_page.next()
        elif self.btn.next() == 2:
            sample_page.next()
        elif self.btn.home() == 2:
            sample_page.next()

    def load(self):
        if self.is_load == False:
            self.is_load = True
            sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.agent = agent()
            self.agent.event(150, self.key_event)
            #self.agent.event(500, sample_page.next)
        else:
            if Report.Key_Test:
                sample_page.next()

    def work(self):
        self.agent.cycle()
        y = 20
        ui.canvas.draw_string(10, y, "5 KeyReport", (127, 255, 255), scale=3)
        y += 40
        ui.canvas.draw_string(10, y, "Home " + ("Pass" if (KeyTest.home_click) else "Fail"), (0, 255, 0) if (KeyTest.home_click) else (255, 0, 0), scale=3)
        y += 40
        ui.canvas.draw_string(10, y, "Back " + ("Pass" if (KeyTest.back_click) else "Fail"), (0, 255, 0) if (KeyTest.back_click) else (255, 0, 0), scale=3)
        y += 40
        ui.canvas.draw_string(10, y, "Next " + ("Pass" if (KeyTest.next_click) else "Fail"), (0, 255, 0) if (KeyTest.next_click) else (255, 0, 0), scale=3)
        y += 40
        ui.canvas.draw_string(10, y, "KeyTest " + ("Pass" if (Report.Key_Test) else "Fail"), (0, 255, 0) if (Report.Key_Test) else (255, 0, 0), scale=3)
        y += 40
        ui.canvas.draw_string(10, y, "Press Any-Key Continue", (255, 255, 255), scale=2)

    def free(self):
        if self.is_load:
            pass
        sample_page.btn.enable = True

class TouchTest():

    def __init__(self, scl=24, sda=27):
        self.is_load = False
        self.scl = scl
        self.sda = sda
        self.i2c = I2C(I2C.I2C4, freq=100*1000, scl=24, sda=27)

    def ft6x36_write_reg(self, reg_addr, buf):
        self.i2c.writeto_mem(0x38, reg_addr, buf, mem_size=8)

    def ft6x36_read_reg(self, reg_addr, buf_len):
        return self.i2c.readfrom_mem(0x38, reg_addr, buf_len, mem_size=8)

    def test_event(self):
        if self.isconnected and self.work_data != None and self.work_data[0] > 0 and self.work_data[1] > 0:
            Report.Touch_Test = True
        sample_page.next()

    def load(self):
        if Report.Touch_Test:
            sample_page.next()
        if self.is_load == False:
            # i2c init()
            sample_page.btn.enable = False
            self.isconnected = False
            self.isError = None
            self.bak = None
            self.work_data = None
            self.agent = agent()
            self.agent.event(500, self.check)
            self.agent.event(8000, self.test_event)
            self.is_load = True

    def free(self):
        if self.is_load:
            # i2c deinit()
            sample_page.btn.enable = True
            self.is_load = False

    def check(self):
        try:
            #print(self.i2c.scan())
            #self.isconnected = True
            if self.isconnected == False:
                #print(self.i2c.scan())
                if 0x38 in self.i2c.scan():
                    self.ft6x36_write_reg(0x00, 0x0)
                    self.ft6x36_write_reg(0x80, 0xC)
                    self.ft6x36_write_reg(0x88, 0xC)
                    self.isconnected = True
            else:
                if self.bak == None and self.work_data != None:
                    self.bak = self.work_data
                if self.bak != None:
                    #print(self.bak, self.work_data)
                    if abs(self.bak[0] - self.work_data[0]) > 80 or abs(self.bak[1] - self.work_data[1]) > 80:
                        Report.Touch_Test = True
                        sample_page.next()

        except Exception as e:
            Report.Touch_Test = False
            Report.isError = str(e)
            print(e)

    def work(self):
        self.agent.parallel_cycle()

        ui.canvas.draw_string(10, 10, "6 Touch Test", (0, 255, 127), scale=2)
        ui.canvas.draw_string(10, 50, "isconnected: %s" % (
            str)(self.isconnected), (255, 127, 0), scale=2)
        if self.isconnected:
            #time.sleep_ms(10)
            data = self.ft6x36_read_reg(0x02, 1)
            #print("reg:" + str(data))
            #if sta & 0x0f: # 读取触摸点的状态
            if (data[0] == 0x1): # 读取触摸点 1 的状态
                data_buf = self.ft6x36_read_reg(0x03, 4)
                y = ((data_buf[0]&0x0f)<<8) | (data_buf[1])
                x = ((data_buf[2]&0x0f)<<8) | (data_buf[3])
                #if ((data_buf[0]&0xc0) == 0x80): # 松开
                #print("point[{}:{}]".format(x,y))
                self.work_data = [x, y]
                #img.draw_rectangle(x + 1, y + 1, x, y, fill=True, color=(0x00, 0x00, 0xff))
                ui.canvas.draw_circle(x - 80, 320 - y, 25, fill=True, color=(0x00, 0x00, 0xff))
                ui.canvas.draw_string(10, int(240 / 2), "point[{}:{}]".format(x,y), (255, 255, 255), scale=3)
        if self.isError != None:
            ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
            sample_page.next()

class TouchReport():

    def __init__(self):
        self.is_load = False

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            sample_page.next()
        elif self.btn.next() == 2:
            sample_page.next()
        elif self.btn.home() == 2:
            sample_page.next()

    def load(self):
        if self.is_load == False:
            self.is_load = True
            sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.agent = agent()
            self.agent.event(150, self.key_event)
            #self.agent.event(2000, sample_page.next)
        else:
            if Report.Touch_Test:
                sample_page.next()

    def work(self):
        self.agent.cycle()
        y = 20
        ui.canvas.draw_string(10, y, "6 TouchReport", (127, 255, 255), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "Touch " + ("Pass" if (Report.Touch_Test) else "Fail"), (0, 255, 0) if (Report.Touch_Test) else (255, 0, 0), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "Press Any-Key Continue", (255, 255, 255), scale=2)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False
        sample_page.btn.enable = True

class FrontSensorTest():

    def __init__(self):
        self.is_load = False
        self.isconnected = False

    def test_event(self):
        if self.get_image != None:
            Report.FrontSensor_Test = True
        sample_page.next()

    def check(self):
        try:
            self.btn.expand_event()

            if self.btn.home() == 2:
                # sipeed_led.w.value(0)
                Report.FrontSensor_Test = True
                sample_page.next()

            if self.isconnected == False:
                try:
                    sensor.reset(choice=2)
                    sensor.set_pixformat(sensor.YUV422)
                    sensor.set_framesize(sensor.QVGA)
                    sensor.run(1)
                    sensor.skip_frames()
                    self.isconnected = True
                    # sipeed_led.w.value(0)
                except Exception as e:
                    Report.FrontSensor_Test = False
                    Report.isError = str(e)
                    print(e)
        except Exception as e:
            Report.FrontSensor_Test = False
            Report.isError = str(e)
            print(e)

    def load(self):
        if Report.FrontSensor_Test:
            sample_page.next()
        if self.is_load == False:
            # sipeed_led.init(14, 15, 17, 32)
            # sipeed_led.w.value(1)
            #sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.get_image = None
            self.isError = None
            self.agent = agent()
            self.agent.event(100, self.check)
            self.agent.event(8000, self.test_event)
            self.is_load = True

    def free(self):
        if self.is_load:
            sample_page.btn.enable = True
            self.is_load = False
            # sipeed_led.w.value(1)

    def work(self):
        self.agent.parallel_cycle()
        if self.isconnected:
            try:
                self.get_image = sensor.snapshot().rotation_corr(x_rotation = 180, z_rotation = +90)
                #ui.canvas.draw_image(self.get_image, 0, 0)
                ui.canvas = self.get_image
            except Exception as e:
                print(e)
        ui.canvas.draw_string(10, 30, "7 FrontSensor Test", (127, 127, 255), scale=3)
        ui.canvas.draw_string(10, 70, "isconnected: %s" % (
            str)(self.isconnected), (255, 127, 0), scale=2)
        if self.isError != None:
            ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
            sample_page.next()

class FrontSensorReport():

    def __init__(self):
        self.is_load = False

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            sample_page.next()
        elif self.btn.next() == 2:
            sample_page.next()
        elif self.btn.home() == 2:
            sample_page.next()

    def load(self):
        if self.is_load == False:
            self.is_load = True
            sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.agent = agent()
            self.agent.event(150, self.key_event)
            #self.agent.event(2000, sample_page.next)
        elif Report.RearSensor_Test:
            sample_page.next()

    def work(self):
        self.agent.cycle()
        y = 20
        ui.canvas.draw_string(10, y, "7 FrontSensorReport", (127, 255, 255), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "FrontSensor " + ("Pass" if (Report.FrontSensor_Test) else "Fail"), (0, 255, 0) if (Report.FrontSensor_Test) else (255, 0, 0), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "Press Any-Key Continue", (255, 255, 255), scale=2)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False
        sample_page.btn.enable = True

class RearSensorTest():

    def __init__(self):
        self.is_load = False
        self.isconnected = False

    def test_event(self):
        if self.get_image != None:
            Report.RearSensor_Test = True
        sample_page.next()

    def check(self):
        try:
            self.btn.expand_event()

            if self.btn.home() == 2:
                sipeed_led.w.value(0)
                Report.RearSensor_Test = True
                sample_page.next()

            if self.isconnected == False:
                try:
                    sensor.reset(choice=1)
                    sensor.set_pixformat(sensor.YUV422)
                    sensor.set_framesize(sensor.QVGA)
                    sensor.set_hmirror(1)
                    sensor.set_vflip(1)
                    sensor.run(1)
                    sensor.skip_frames()
                    self.isconnected = True
                    sipeed_led.w.value(0)
                except Exception as e:
                    Report.RearSensor_Test = False
                    Report.isError = str(e)
                    print(e)
        except Exception as e:
            Report.RearSensor_Test = False
            Report.isError = str(e)
            print(e)

    def load(self):
        if Report.RearSensor_Test:
            sample_page.next()
        if self.is_load == False:
            sipeed_led.init(14, 15, 17, 32)
            sipeed_led.w.value(1)
            #sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.get_image = None
            self.isError = None
            self.agent = agent()
            self.agent.event(150, self.check)
            self.agent.event(8000, self.test_event)
            self.is_load = True

    def free(self):
        if self.is_load:
            sample_page.btn.enable = True
            self.is_load = False
            sipeed_led.w.value(1)

    def work(self):
        self.agent.parallel_cycle()
        if self.isconnected:
            try:
                self.get_image = sensor.snapshot()
                #ui.canvas.draw_image(self.get_image, 0, 0)
                ui.canvas = (self.get_image)
            except Exception as e:
                print(e)
        ui.canvas.draw_string(10, 30, "8 RearSensor Test", (127, 127, 255), scale=3)
        ui.canvas.draw_string(10, 70, "isconnected: %s" % (
            str)(self.isconnected), (255, 127, 0), scale=2)
        if self.isError != None:
            ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
            sample_page.next()

class RearSensorReport():

    def __init__(self):
        self.is_load = False

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            sample_page.next()
        elif self.btn.next() == 2:
            sample_page.next()
        elif self.btn.home() == 2:
            sample_page.next()

    def load(self):
        if self.is_load == False:
            self.is_load = True
            sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.agent = agent()
            self.agent.event(150, self.key_event)
            #self.agent.event(2000, sample_page.next)
        elif Report.RearSensor_Test:
            sample_page.next()

    def work(self):
        self.agent.cycle()
        y = 20
        ui.canvas.draw_string(10, y, "8 RearSensorReport", (127, 255, 255), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "RearSensor " + ("Pass" if (Report.RearSensor_Test) else "Fail"), (0, 255, 0) if (Report.RearSensor_Test) else (255, 0, 0), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "Press Any-Key Continue", (255, 255, 255), scale=2)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False
        sample_page.btn.enable = True

class AudioTest():

    PlayTest = False
    RecordTest = False

    def __init__(self):
        self.is_load = False
        self.i2c = I2C(I2C.I2C4, freq=100*1000, scl=24, sda=27)
        CubeAudio.init(self.i2c)
        self.count = 0

    def load(self):
        if Report.Audio_Test:
            sample_page.next()
        if self.is_load == False:
            # i2c init()
            sample_page.btn.enable = False
            self.isconnected = False
            self.isError = None
            self.is_play = False
            self.is_record = False
            self.state = 0
            self.fft_amp = None
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.count += 1
            self.agent = agent()
            self.agent.event(150, self.key_event)
            self.agent.event(500, self.check)
            self.agent.event(16000, self.test_event)
            self.is_load = True

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2 or self.btn.next() == 2:
            if self.state == 0:
                AudioTest.PlayTest = False
            if self.state == 2:
                AudioTest.RecordTest = False
            self.state += 1
        elif self.btn.home() == 2:
            if self.state == 0:
                AudioTest.PlayTest = True
            if self.state == 2:
                AudioTest.RecordTest = True
            self.state += 1
        if self.state > 2:
            sample_page.next()

    def test_event(self):
        if self.state == 0 or self.state == 2:
            self.state += 1

    def free(self):
        if self.is_load:
            # i2c deinit()
            sample_page.btn.enable = True
            self.is_load = False

    def check(self):
        try:
            if self.isconnected == False:
                self.isconnected = CubeAudio.check()
            else:
                if self.state == 0 and self.is_play == False:
                    self.is_play = True
                    CubeAudio.ready()
                    from fpioa_manager import fm
                    fm.register(13,fm.fpioa.I2S0_MCLK, force=True)
                    fm.register(21,fm.fpioa.I2S0_SCLK, force=True)
                    fm.register(18,fm.fpioa.I2S0_WS, force=True)
                    fm.register(35,fm.fpioa.I2S0_IN_D0, force=True)
                    fm.register(34,fm.fpioa.I2S0_OUT_D2, force=True)
                    # CubeAudio.i2s.set_sample_rate(22050)
                elif self.state == 1 and self.is_record == False:
                    self.is_record = True
                    CubeAudio.ready(True)
                    CubeAudio.i2s.set_sample_rate(22050)
        except Exception as e:
            #Report.Audio_Test = False
            Report.isError = str(e)
            print(e)

    def work(self):
        self.agent.parallel_cycle()

        ui.canvas.draw_string(10, 30, "9 Audio Test", (127, 127, 255), scale=3)
        ui.canvas.draw_string(10, 70, "isconnected: %s" % (
            str)(self.isconnected), (255, 127, 0), scale=2)

        ui.canvas.draw_string(10, 100, "Test: %s" %
            ('play' if self.state == 0 else 'record'), (255, 127, 0), scale=3)

        #print(time.ticks_ms())

        if self.isconnected:
            if self.state == 0 and self.is_play:
                if CubeAudio.event() == False:
                    CubeAudio.load(os.getcwd() + "/res/sound/loop.wav", 100)
                    #print('self.count', self.count)
                    if self.count > 1:
                        CubeAudio.i2s.set_sample_rate(22050)
                    else:
                        # pass
                        CubeAudio.i2s.set_sample_rate(22050)
            elif self.state == 1:
                ui.canvas.draw_string(10, 200, "Press Any-Key \n Start", (255, 127, 0), scale=3)
            elif self.state == 2 and self.is_record:
                tmp = CubeAudio.i2s.record(1024)
                fft_res = FFT.run(tmp.to_bytes(), 512)
                fft_amp = FFT.amplitude(fft_res)
                if fft_amp[50] > 100 and fft_amp[100] > 100:
                    AudioTest.RecordTest = True
                    sample_page.next()
                for x_shift in range(240):
                    hist_height = fft_amp[x_shift]
                    ui.canvas.draw_rectangle((x_shift, 0, 1, hist_height), [255,255,255], 1, True)
                    #print((x_shift, 0, 1, hist_height))

        if self.isError != None:
            ui.canvas.draw_string(40, 80, self.isError, (255, 255, 255), scale=2)
            sample_page.next()

class AudioReport():

    def __init__(self):
        self.is_load = False

    def key_event(self):
        self.btn.expand_event()

        if self.btn.back() == 2:
            sample_page.next()
        elif self.btn.next() == 2:
            sample_page.next()
        elif self.btn.home() == 2:
            sample_page.next()

    def load(self):
        if self.is_load == False:
            self.is_load = True
            sample_page.btn.enable = False
            self.btn = sipeed_button()
            # self.btn.config(23, 20, 31)
            self.agent = agent()
            self.agent.event(150, self.key_event)
            #self.agent.event(500, sample_page.next)
        elif Report.Audio_Test:
            sample_page.next()

        Report.Audio_Test = False
        if AudioTest.PlayTest and AudioTest.RecordTest:
            Report.Audio_Test = True

    def work(self):
        self.agent.cycle()
        y = 20
        ui.canvas.draw_string(10, y, "9 AudioReport", (127, 255, 255), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "PlayTest " + ("Pass" if (AudioTest.PlayTest) else "Fail"), (0, 255, 0) if (AudioTest.PlayTest) else (255, 0, 0), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "Record " + ("Pass" if (AudioTest.RecordTest) else "Fail"), (0, 255, 0) if (AudioTest.RecordTest) else (255, 0, 0), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "Audio " + ("Pass" if (Report.Audio_Test) else "Fail"), (0, 255, 0) if (Report.Audio_Test) else (255, 0, 0), scale=3)
        y += 50
        ui.canvas.draw_string(10, y, "Press Any-Key Continue", (255, 255, 255), scale=2)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False
        sample_page.btn.enable = True

class SdcardTest():

    def __init__(self):
        self.is_load = False
        self.load()

    def load(self):
        if self.is_load == False:
            self.is_load = True
            self.result = os.getcwd() == '/sd' # and len(os.listdir('/sd')) > 0
            self.agent = agent()
            self.agent.event(500, sample_page.next)
        else:
            sample_page.next()

    def work(self):
        self.agent.cycle()
        ui.canvas.draw_string(10, 20, "SdCardTest", (127, 255, 255), scale=3)
        ui.canvas.draw_string(30, 120, "Pass" if (self.result) else "Fail", (0, 255, 0) if (self.result) else (255, 0, 0), scale=8)

        ui.canvas.draw_string(30, 260, "Start Test", (0, 0, 255), scale=3)

    def free(self):
        if self.is_load:
            pass
            #self.is_load = False

if __name__ == "__main__":
    import json

    amigo = {
    "type": "amigo",
    "lcd": {
        "height": 320,
        "width": 480,
        "invert": 0,
        "dir": 40,
        "lcd_type": 1
    },
    "sdcard":{
        "sclk":11,
        "mosi":10,
        "miso":6,
        "cs":26
    },
    "freq_cpu": 416000000,
    "freq_pll1": 400000000,
    "kpu_div": 1
    }


    data = amigo

    cfg = json.dumps(data)
    #print(cfg)

    try:
      with open('/flash/config.json', 'rb') as f:
        tmp = json.loads(f.read())
        print(tmp)
        if tmp["type"] != data["type"]:
          raise Exception('config.json no exist')
    except Exception as e:
      with open('/flash/config.json', "w") as f:
        f.write(cfg)
      import machine
      machine.reset()

    protect.keep()

    import time, gc
    # gc.collect()
    # gc.collect()
    if len(sample_page.samples) > 0:
        sample_page.samples = []
        # gc.collect()

    button_io.config(23, 31, 20) # old
    button_io.config(16, 23, 20) # new
    sample_page.key_init()

    sample_page.add_sample(Report()) # keep

    sample_page.add_sample(AudioReport())
    sample_page.add_sample(AudioTest())

    sample_page.add_sample(RearSensorReport())
    sample_page.add_sample(RearSensorTest())

    sample_page.add_sample(FrontSensorReport())
    sample_page.add_sample(FrontSensorTest())

    sample_page.add_sample(TouchReport())
    sample_page.add_sample(TouchTest())

    sample_page.add_sample(KeyReport())
    sample_page.add_sample(KeyTest())

    sample_page.add_sample(WaitTestStart())

    # sample_page.add_sample(SpmodReport())
    # sample_page.add_sample(SpmodTest(30, 28, 29, 8))
    # sample_page.add_sample(SpmodTest(10, 6, 12, 11))

    # sample_page.add_sample(GroveReport())
    # sample_page.add_sample(GroveTest())

    sample_page.add_sample(Msa301Report())
    sample_page.add_sample(Msa301Test())

    sample_page.add_sample(PowerReport())
    sample_page.add_sample(PowerTest())

    sample_page.add_sample(SdcardTest()) # keep

    #ui.height, ui.weight = int(lcd.width() / 2), int(lcd.height())

    ui.height, ui.weight = 280, 280

    @ui.warp_template(ui.blank_draw)
    #@ui.warp_template(ui.grey_draw)
    @ui.warp_template(sample_page.sample_draw)
    def app_main():
        ui.display()

    import time
    last = time.ticks_ms() - 1
    while True:
        last = time.ticks_ms()
        app_main()
        protect.keep()
        #print((int)(1000 / (time.ticks_ms() - last)), 'fps')
        continue
        while True:
            app_main()
            protect.keep()
            continue
            try:
                print((int)(1000 / (time.ticks_ms() - last)), 'fps')
                last = time.ticks_ms()
                app_main()
                protect.keep()
                #print(time.ticks_ms(), 'ram total : ' + str(gc.mem_free() / 1024) + ' kb')
                #time.sleep(0.1)
            except KeyboardInterrupt:
                protect.stop()
                raise KeyboardInterrupt()
            except MemoryError as e:
                print(time.ticks_ms(), 'ram total : ' + str(gc.mem_free() / 1024) + ' kb')
                #print(e)
            except Exception as e:
                print(e)
