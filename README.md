# MicroPython-Samples [![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg?style=for-the-badge)](./LICENSE)

This is the MicroPython UI framework.

- Decoration design
- Support layer drawing
- Support event-driven model
- No function overloading is required
- Provide basic framework examples

Enjoy it!

## Architecture description

Explain with code.

### Layer drawing

For example, implement a status(taskbar) bar.

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

- bg_in_draw
  - time xxms
  - mem xxkb

- anime_in_draw
  - time xxms
  - mem xxkb

- bg_draw
  - time xxms
  - mem xxkb

- anime_draw
  - time xxms
  - mem xxkb

- system_info
  - time xxms
  - mem xxkb

- taskbar
  - time xxms
  - mem xxkb
