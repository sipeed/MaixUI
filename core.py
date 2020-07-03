import _thread, time

class Core:

    log, thread, task, interval, state = print, None, None, 0, False

    def debug(enable):
        Core.log = print if enable else lambda *args:None

    def callback(func, inte=0.5):
        Core.task, Core.interval = func, inte

    def background():
        try:
            while Core.state:
                if Core.task:
                    try:
                        Core.task()
                    except Exception as e:
                        print(e)
                time.sleep(Core.interval)
            Core.log(Core.background, time.time())
        except Exception as e:
            print(e)
        finally:
            Core.state = True

    def quit():
        if Core.state == True:
            Core.state = False
            if Core.thread != None:
                while Core.state != True:
                    time.sleep(1) # wait _thread exit
                Core.thread = None
        Core.log(Core.quit, time.time())

    def run(): # maybe re-entry
        Core.quit()
        if Core.state == False:
            Core.state, Core.thread = True, _thread.start_new_thread(Core.background, ())
        Core.log(Core.run, time.time())

Core.run() # import enable

# execfile('core.py')
# execfile('ui.py')