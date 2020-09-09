from machine import I2C
from fpioa_manager import fm
from micropython import const
import struct, time


# [4|5] [7  |VCC]
# [3|6] [15 | 21]
# [2|7] [20 |  8]
# [1|8] [GND|  6]

#SDA -> 7
#SHT -> 8
#IRQ -> 20
#SCL -> 6

i2c = I2C(I2C.I2C0, freq=100000, scl=6, sda=7)
devices = i2c.scan()
fm.register(8, fm.fpioa.GPIOHS0, force=True)
XSHUT = GPIO(GPIO.GPIOHS0, GPIO.OUT)
XSHUT.value(1)

address = 0x29
print(address, devices)

def bswap(val):
    return struct.unpack('<H', struct.pack('>H', val))[0]
def mread_word_data(adr, reg):
    return bswap(bus.read_word_data(adr, reg))
def mwrite_word_data(adr, reg, data):
    return bus.write_word_data(adr, reg, bswap(data))
def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)
def VL53L0X_decode_vcsel_period(vcsel_period_reg):
# Converts the encoded VCSEL period register value into the real
# period in PLL clocks
    vcsel_period_pclks = (vcsel_period_reg + 1) << 1;
    return vcsel_period_pclks;

VL53L0X_REG_IDENTIFICATION_MODEL_ID		= 0x00c0
VL53L0X_REG_IDENTIFICATION_REVISION_ID		= 0x00c2
VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD	= 0x0050
VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD	= 0x0070
VL53L0X_REG_SYSRANGE_START			= 0x000

VL53L0X_REG_RESULT_INTERRUPT_STATUS 		= 0x0013
VL53L0X_REG_RESULT_RANGE_STATUS 		= 0x0014

val1 = i2c.readfrom_mem(address, VL53L0X_REG_IDENTIFICATION_REVISION_ID, 1, mem_size=8)[0]

print("Revision ID: " + hex(val1))
val1 = i2c.readfrom_mem(address, VL53L0X_REG_IDENTIFICATION_MODEL_ID, 1, mem_size=8)[0]


print("Device ID: " + hex(val1))
#	case VL53L0X_VCSEL_PERIOD_PRE_RANGE:
#		Status = VL53L0X_RdByte(Dev,
#			VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD,
#			&vcsel_period_reg);
val1 = i2c.readfrom_mem(address, VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD, 1, mem_size=8)[0]

print("PRE_RANGE_CONFIG_VCSEL_PERIOD=" + hex(val1) + " decode: " + str(VL53L0X_decode_vcsel_period(val1)))


while True:
    time.sleep(0.25)

    #	case VL53L0X_VCSEL_PERIOD_FINAL_RANGE:
    #		Status = VL53L0X_RdByte(Dev,
    #			VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD,
    #			&vcsel_period_reg);

    val1 = i2c.readfrom_mem(address, VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD, 1, mem_size=8)[0]

    print("FINAL_RANGE_CONFIG_VCSEL_PERIOD=" + hex(val1) + " decode: " + str(VL53L0X_decode_vcsel_period(val1)))

    #		Status = VL53L0X_WrByte(Dev, VL53L0X_REG_SYSRANGE_START, 0x01);
    val1 = i2c.writeto_mem(address, VL53L0X_REG_SYSRANGE_START, 0x01)

    #		Status = VL53L0X_RdByte(Dev, VL53L0X_REG_RESULT_RANGE_STATUS,
    #			&SysRangeStatusRegister);
    #		if (Status == VL53L0X_ERROR_NONE) {
    #			if (SysRangeStatusRegister & 0x01)
    #				*pMeasurementDataReady = 1;
    #			else
    #				*pMeasurementDataReady = 0;
    #		}
    cnt = 0
    while (cnt < 100): # 1 second waiting time max
      time.sleep(0.010)
      val = i2c.readfrom_mem(address, VL53L0X_REG_RESULT_RANGE_STATUS, 1, mem_size=8)[0]
      if (val & 0x01):
        break
      cnt += 1

    if (val & 0x01):
      print("ready")
    else:
      print("not ready")

    #	Status = VL53L0X_ReadMulti(Dev, 0x14, localBuffer, 12);
    data = i2c.readfrom_mem(address, 0x14, 12, mem_size=8)

    print(data)
    print("ambient count " + str(makeuint16(data[7], data[6])))
    print("signal count " + str(makeuint16(data[9], data[8])))
    #		tmpuint16 = VL53L0X_MAKEUINT16(localBuffer[11], localBuffer[10]);
    print("distance " + str(makeuint16(data[11], data[10])))

    DeviceRangeStatusInternal = ((data[0] & 0x78) >> 3)
    print(DeviceRangeStatusInternal)

'''
FINAL_RANGE_CONFIG_VCSEL_PERIOD=0x5 decode: 12
ready
b'A\x06\xb9\x00\x00\x03\x00\x08\x00\x8b\x00\x14'ambient count 8
signal count 139
distance 20
'''
