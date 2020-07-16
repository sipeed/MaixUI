
from machine import WDT

class protect:
    wdt = None
    def start():
        protect.wdt = WDT(id=0, timeout=6000) # protect.stop()
    def keep():
        protect.wdt.feed()
    def stop():
        protect.wdt.stop()

protect.start()
