# The MIT License (MIT)
#
# Copyright (c) 2017 ladyada for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# We have a lot of attributes for this complex sensor.
# pylint: disable=too-many-instance-attributes

"""
`adafruit_bme680` - Adafruit BME680 - Temperature, Humidity, Pressure & Gas Sensor
===================================================================================
CircuitPython driver from BME680 air quality sensor
* Author(s): ladyada
"""

import time
import math
from micropython import const
from ubinascii import hexlify as hex
try:
    import struct
except ImportError:
    import ustruct as struct

#    I2C ADDRESS/BITS/SETTINGS
#    -----------------------------------------------------------------------
_BME680_CHIPID = const(0x61)

_BME680_REG_CHIPID = const(0xD0)
_BME680_BME680_COEFF_ADDR1 = const(0x89)
_BME680_BME680_COEFF_ADDR2 = const(0xE1)
_BME680_BME680_RES_HEAT_0 = const(0x5A)
_BME680_BME680_GAS_WAIT_0 = const(0x64)

_BME680_REG_SOFTRESET = const(0xE0)
_BME680_REG_CTRL_GAS = const(0x71)
_BME680_REG_CTRL_HUM = const(0x72)
_BME280_REG_STATUS = const(0xF3)
_BME680_REG_CTRL_MEAS = const(0x74)
_BME680_REG_CONFIG = const(0x75)

_BME680_REG_PAGE_SELECT = const(0x73)
_BME680_REG_MEAS_STATUS = const(0x1D)
_BME680_REG_PDATA = const(0x1F)
_BME680_REG_TDATA = const(0x22)
_BME680_REG_HDATA = const(0x25)

_BME680_SAMPLERATES = (0, 1, 2, 4, 8, 16)
_BME680_FILTERSIZES = (0, 1, 3, 7, 15, 31, 63, 127)

_BME680_RUNGAS = const(0x10)

_LOOKUP_TABLE_1 = (2147483647, 2147483647, 2147483647, 2147483647, 2147483647,
                   2126008810, 2147483647, 2130303777, 2147483647, 2147483647,
                   2143188679, 2136746228, 2147483647, 2126008810, 2147483647,
                   2147483647)

_LOOKUP_TABLE_2 = (4096000000, 2048000000, 1024000000, 512000000, 255744255, 127110228,
                   64000000, 32258064, 16016016, 8000000, 4000000, 2000000, 1000000,
                   500000, 250000, 125000)


def _read24(arr):
    """Parse an unsigned 24-bit value as a floating point and return it."""
    ret = 0
    #print([hex(i) for i in arr])
    for b in arr:
        ret <<= 8
        ret += b & 0xFF
    return ret


class Adafruit_BME680:
    """Driver from BME680 air quality sensor
       :param int refresh_rate: Maximum number of readings per second. Faster property reads
         will be from the previous reading."""
    def __init__(self, *, refresh_rate=10):
        """Check the BME680 was found, read the coefficients and enable the sensor for continuous
           reads."""
        self._write(_BME680_REG_SOFTRESET, [0xB6])
        time.sleep(0.005)

        # Check device ID.
        chip_id = self._read_byte(_BME680_REG_CHIPID)
        if chip_id != _BME680_CHIPID:
            raise RuntimeError('Failed to find BME680! Chip ID 0x%x' % chip_id)

        self._read_calibration()

        # set up heater
        self._write(_BME680_BME680_RES_HEAT_0, [0x73])
        self._write(_BME680_BME680_GAS_WAIT_0, [0x65])

        self.sea_level_pressure = 1013.25
        """Pressure in hectoPascals at sea level. Used to calibrate ``altitude``."""

        # Default oversampling and filter register values.
        self._pressure_oversample = 0b011
        self._temp_oversample = 0b100
        self._humidity_oversample = 0b010
        self._filter = 0b010

        self._adc_pres = None
        self._adc_temp = None
        self._adc_hum = None
        self._adc_gas = None
        self._gas_range = None
        self._t_fine = None

        self._last_reading = 0
        self._min_refresh_time = 1000 / refresh_rate

    @property
    def pressure_oversample(self):
        """The oversampling for pressure sensor"""
        return _BME680_SAMPLERATES[self._pressure_oversample]

    @pressure_oversample.setter
    def pressure_oversample(self, sample_rate):
        if sample_rate in _BME680_SAMPLERATES:
            self._pressure_oversample = _BME680_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")

    @property
    def humidity_oversample(self):
        """The oversampling for humidity sensor"""
        return _BME680_SAMPLERATES[self._humidity_oversample]

    @humidity_oversample.setter
    def humidity_oversample(self, sample_rate):
        if sample_rate in _BME680_SAMPLERATES:
            self._humidity_oversample = _BME680_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")

    @property
    def temperature_oversample(self):
        """The oversampling for temperature sensor"""
        return _BME680_SAMPLERATES[self._temp_oversample]

    @temperature_oversample.setter
    def temperature_oversample(self, sample_rate):
        if sample_rate in _BME680_SAMPLERATES:
            self._temp_oversample = _BME680_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")

    @property
    def filter_size(self):
        """The filter size for the built in IIR filter"""
        return _BME680_FILTERSIZES[self._filter]

    @filter_size.setter
    def filter_size(self, size):
        if size in _BME680_FILTERSIZES:
            self._filter = _BME680_FILTERSIZES[size]
        else:
            raise RuntimeError("Invalid size")

    @property
    def temperature(self):
        """The compensated temperature in degrees celsius."""
        self._perform_reading()
        calc_temp = (((self._t_fine * 5) + 128) // 256)
        return calc_temp / 100

    @property
    def pressure(self):
        """The barometric pressure in hectoPascals"""
        self._perform_reading()
        
        var1 = (int(self._t_fine) >> 1) - 64000
        var2 = ((var1 >> 2) * (var1 >> 2 )) >> 11
        var2 = (var2 * self._pressure_calibration[5]) >> 2
        var2 = var2 + ((var1 * self._pressure_calibration[4]) << 1)
        var2 = (var2 >> 2) + (self._pressure_calibration[3] << 16)
        var1 = (((((var1 >> 2) * (var1 >> 2)) >> 13) *
                (self._pressure_calibration[2] << 5) >> 3) +
                ((self._pressure_calibration[1] * var1) >> 1))
        var1 = var1 >> 18
        var1 = ((32768 + var1) * self._pressure_calibration[0]) >> 15
        calc_pres = 1048576 - int(self._adc_pres)
        calc_pres = (calc_pres - (var2 >> 12)) * 3125
        calc_pres = (calc_pres << 1) // var1
        var1 = (self._pressure_calibration[8] * (((calc_pres >> 3) * (calc_pres >> 3)) >> 13)) >> 12
        var2 = ((calc_pres >> 2) * self._pressure_calibration[7]) >> 13
        var3 = (((calc_pres >> 8) * (calc_pres >> 8) * (calc_pres >> 8)) * self._pressure_calibration[9]) >> 17
        calc_pres += ((var1 + var2 + var3 + (self._pressure_calibration[6] << 7)) >> 4)
        return calc_pres / 100

    @property
    def humidity(self):
        """The relative humidity in RH %"""
        self._perform_reading()

        temp_scaled = ((self._t_fine * 5) + 128) >> 8
        var1 = ((self._adc_hum - (self._humidity_calibration[0] * 16)) -
                (((temp_scaled * self._humidity_calibration[2]) // 100) >> 1))
        var2 = (self._humidity_calibration[1] *
                (((temp_scaled * self._humidity_calibration[3]) // 100) +
                 (((temp_scaled * ((temp_scaled * self._humidity_calibration[4]) 
                    // 100)) >> 6) // 100) + 16384)) >> 10
        var3 = var1 * var2
        var4 = self._humidity_calibration[5] << 7
        var4 = (var4 + ((temp_scaled * self._humidity_calibration[6]) // 100)) >> 4
        var5 = ((var3 >> 14) * (var3 >> 14)) >> 10
        var6 = (var4 * var5) >> 1
        calc_hum = ((var3 + var6) >> 10) / 4096 

        if calc_hum > 10000:
            calc_hum = 10000
        if calc_hum < 0:
            calc_hum = 0
        return calc_hum

    @property
    def altitude(self):
        """The altitude based on current ``pressure`` vs the sea level pressure
           (``sea_level_pressure``) - which you must enter ahead of time)"""
        pressure = self.pressure # in Si units for hPascal
        return 44330 * (1.0 - math.pow(pressure / self.sea_level_pressure, 0.1903))

    @property
    def gas(self):
        """The gas resistance in ohms"""
        self._perform_reading()
        var1 = ((1340 + (5 * self._sw_err)) * (_LOOKUP_TABLE_1[self._gas_range])) >> 16
        var2 = ((self._adc_gas << 15) - 16777216) + var1
        var3 = (_LOOKUP_TABLE_2[self._gas_range] * var1) >> 9
        calc_gas_res = (var3 + (var2 >> 1)) // var2
        return int(calc_gas_res)

    def _perform_reading(self):
        """Perform a single-shot reading from the sensor and fill internal data structure for
           calculations"""
        if (time.ticks_diff(self._last_reading, time.ticks_ms()) * time.ticks_diff(0, 1)
                < self._min_refresh_time):
            return

        # set filter
        self._write(_BME680_REG_CONFIG, [self._filter << 2])
        # turn on temp oversample & pressure oversample
        self._write(_BME680_REG_CTRL_MEAS,
                    [(self._temp_oversample << 5)|(self._pressure_oversample << 2)])
        # turn on humidity oversample
        self._write(_BME680_REG_CTRL_HUM, [self._humidity_oversample])
        # gas measurements enabled
        self._write(_BME680_REG_CTRL_GAS, [_BME680_RUNGAS])

        ctrl = self._read_byte(_BME680_REG_CTRL_MEAS)
        ctrl = (ctrl & 0xFC) | 0x01  # enable single shot!
        self._write(_BME680_REG_CTRL_MEAS, [ctrl])
        new_data = False
        while not new_data:
            data = self._read(_BME680_REG_MEAS_STATUS, 15)
            new_data = data[0] & 0x80 != 0
            time.sleep(0.005)
        self._last_reading = time.ticks_ms()

        self._adc_pres = _read24(data[2:5]) / 16
        self._adc_temp = _read24(data[5:8]) / 16
        self._adc_hum = struct.unpack('>H', bytes(data[8:10]))[0]
        self._adc_gas = int(struct.unpack('>H', bytes(data[13:15]))[0] / 64)
        self._gas_range = data[14] & 0x0F

        var1 = (int(self._adc_temp) >> 3) - (self._temp_calibration[0] << 1)
        var2 = (var1 * self._temp_calibration[1]) >> 11
        var3 = ((var1 >> 1) * (var1 >> 1)) >> 12
        var3 = (var3 * self._temp_calibration[2] << 4) >> 14
        self._t_fine = int(var2 + var3)

    def _read_calibration(self):
        """Read & save the calibration coefficients"""
        coeff = self._read(_BME680_BME680_COEFF_ADDR1, 25)
        coeff += self._read(_BME680_BME680_COEFF_ADDR2, 16)

        coeff = list(struct.unpack('<hbBHhbBhhbbHhhBBBHbbbBbHhbb', bytes(coeff[1:39])))
        # print("\n\n",coeff)
        self._temp_calibration = [coeff[x] for x in [23, 0, 1]]
        self._pressure_calibration = [coeff[x] for x in [3, 4, 5, 7, 8, 10, 9, 12, 13, 14]]
        self._humidity_calibration = [coeff[x] for x in [17, 16, 18, 19, 20, 21, 22]]
        self._gas_calibration = [coeff[x] for x in [25, 24, 26]]

        # flip around H1 & H2
        self._humidity_calibration[1] <<= 4
        self._humidity_calibration[1] |= self._humidity_calibration[0] & 0x0f
        self._humidity_calibration[0] >>= 4

        self._heat_range = (self._read_byte(0x02) & 0x30) >> 4
        self._heat_val = self._read_byte(0x00)
        self._sw_err = (self._read_byte(0x04) & 0xF0) >> 4

    def _read_byte(self, register):
        """Read a byte register value and return it"""
        return 