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

cube = {
  "type": "cube",
  "lcd": {
      "height": 240,
      "width": 240,
      "invert": 1,
      "dir": 96
  },
  "freq_cpu": 416000000,
  "freq_pll1": 400000000,
  "kpu_div": 1
}

data = amigo
#data = cube

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

