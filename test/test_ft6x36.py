
class ft6x36:

  def __init__(self, i2c, w, h):
    self.i2c = i2c
    self.write_reg(0x00, 0x0)
    self.write_reg(0x80, 0xC)
    self.write_reg(0x88, 0xC)
    self.width, self.height = w, h

  def write_reg(self, reg_addr, buf):
    self.i2c.writeto_mem(0x38, reg_addr, buf, mem_size=8)

  def read_reg(self, reg_addr, buf_len):
    return self.i2c.readfrom_mem(0x38, reg_addr, buf_len, mem_size=8)

  def get_point(self):
    data = self.read_reg(0x02, 1)
    print("get_point:" + str(data))
    if (data[0] == 0x1):
        data_buf = self.read_reg(0x03, 4)
        y = ((data_buf[0] & 0x0f) << 8) | (data_buf[1])
        x = ((data_buf[2] & 0x0f) << 8) | (data_buf[3])
        print("1 point[{}:{}]".format(x,y))
        if ((data_buf[0] & 0xc0) == 0x80):
            print("2 point[({},{}):({},{})]".format(
                x, y,  self.width - x, self.height - y))
            return (x, y, self.width - x, self.height - y)
    return None

if __name__ == "__main__":

  import lcd, image, time
  from machine import I2C

  i2c = I2C(I2C.I2C1, freq=100*1000, scl=24, sda=27)
  devices = i2c.scan()
  print(devices)
  tmp = ft6x36(i2c, 640, 320)
  while 1:
    print(tmp.get_point())
    time.sleep(0.5)
