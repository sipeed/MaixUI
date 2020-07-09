# MicroPython-Samples

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

This is the MicroPython UI framework.

- Decoration design
- Support layer drawing
- Support event-driven model
- No function overloading is required
- Provide basic framework examples

Enjoy it!

## Get-started

It is recommended to use app_micro.py as a migration reference for other hardware, it will not contain external images.

use this [app/app_micro.py](app/app_micro.py)

- Ask questions to [issue](https://github.com/sipeed/MaixUI/issues)

- Source archive to [release](https://github.com/sipeed/MaixUI/release)

## Demo effect



## Architecture description

Explain with code.

### Layer drawing

For example, implement a status(taskbar) bar base ui_maix.ui.

```python

import time, gc

from ui_maix import ui

class taskbar:

  now = ''

  def time_draw():
    now = 45678 + time.ticks() / 1000
    taskbar.now = time.localtime(int(now))
    ui.img.draw_string(60, 2, "%02u:%02u:%02u" % (taskbar.now[3], taskbar.now[4], taskbar.now[5]), scale=2)

  def mem_draw():
    info = 'GC %s KB' % str(gc.mem_free() / 1024)
    ui.img.draw_string(10, 2, info, scale=2)

if __name__ == "__main__":

    @ui.warp_template(ui.bg_draw)
    @ui.warp_template(taskbar.mem_draw)
    def app_main():
        ui.display()
    import time
    while True:
        app_main()
        #time.sleep(0.5)
```

This means that the taskbar(taskbar.mem_draw) is drawn after the background(ui.bg_draw) image is drawn.

look at this [ui/ui_user.py](ui/ui_user.py)

### Page design

The difference is that it can be used multiple times, so object-oriented design is required.

```python

class user:

  def __init__(self):
    self.btn = cube_button()
    self.page_info = sys_info()
    self.page = 0

  def draw(self):
    self.btn.event()

    if self.btn.back() == 1:
        self.page -= 1
    elif self.btn.next() == 1:
        self.page += 1
    self.page = self.page % 3

    if self.page == 0:
      ui.img.draw_string(20, 30, "Weclome to MaixCube", (255, 255, 127), scale=2)
    if self.page == 1:
      self.page_info.draw(ui.img)
    if self.page == 2:
      ui.img.draw_string(40, 200, "Enjoy it! :D", (255, 0, 127), scale=2)

```

look at this [ui/ui_user.py](ui/ui_user.py)

### Event-driven

Note that many events are not implemented for users to reload, in fact it is tailorable and not necessary.

> Please do not use the following design.

```python

class bar(frame):
  
  def on_button_press():
    pass
  
  def on_button_release():
    pass

```

For example, our button driver realizes the event of pressing and releasing, and can give any function to actively access the button event.

```python

class bar(frame):

  btn = button()

  def draw(): # Cycle run

    bar.btn.event() # It can be performed elsewhere.

    if bar.btn.next() = 1: # button press
      pass
    if bar.btn.back() = 2: # button release
      pass
    if bar.btn.home():
      pass

```

Similarly other.

look at this [driver/button.py](driver/button.py)

### driver programming

Simple can be written like this.

```python
import sys, time
import sensor, lcd

def camera_init():
    sensor.run(1)

def get_image():
    return sensor.snapshot()

try:
    camera_init()
except Exception as e:
    time.sleep(1)
    camera_init()

if __name__ == "__main__":
    pass
```

import will help you perform the first time.

look at this [driver/camera.py](driver/camera.py)

But this is not reliable.

### Unit-Test

Please make sure that each code can be unit tested.

```python

class test:

    def hello():
      pass

if __name__ == "__main__":
    test.hello()

```

This also facilitates the splitting of components, which facilitates independent commissioning and optimization.

### Optimization

Control memory usage and refresh rate.

#### FPS

- Compatible with CPython

```python

  import time
  last = time.ticks_ms()
  while True:
      try:
          print(time.ticks_ms() - last)
          last = time.ticks_ms()
          your_func()
      except Exception as e:
          print(e)

```

- MaixPy only

```python

  clock = time.clock()
  while(True):
      clock.tick()
      lcd.display(get_image())
      print(clock.fps())
      print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')
      kpu.memtest()

```

#### View remaining memory

```python

def print_mem_free():
    print('ram total : ' + str(gc.mem_free() / 1024) + ' kb')

import gc, image

print_mem_free()

tmp = ' '*4096

print_mem_free()

del tmp

print_mem_free()

'''
ram total : 989.4375 kb
ram total : 985.0625 kb
ram total : 984.8437 kb
'''

```

Next up to you.

## Performance statistics

Record the time and memory usage of each component.

- ui_maix.py
  - bg_in_draw
  - anime_in_draw
  - need 35ms (28fps)
  - need mem xxxkb

- app_micro.py
  - bg_draw
  - anime_draw
  - system_info
  - taskbar
  - need 30 ~ 51ms (20 ~ 28fps)
  - need mem 330kb

## Precautions

请注意组件可重用性和绘图性能测试，必须保证每个模块均有开发过程产生的单元测试。

Please note that component reusability and graphics performance testing must ensure that each module has unit tests generated during the development process.

请确保页面只是对 UI 元素的描述和交互，所以可以在页面交互逻辑中实现业务逻辑、绘图逻辑，但不允许存在驱动逻辑，这也是为了在 CPython 里同步实现。

Please ensure that the page is only the description and interaction of UI elements, so you can implement business logic and drawing logic in the page interaction logic, but there is no hardware driving logic allowed. This is also for synchronous implementation in CPython.
