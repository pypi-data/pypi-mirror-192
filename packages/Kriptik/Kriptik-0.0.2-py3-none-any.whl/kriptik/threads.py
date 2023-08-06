import threading
import time

class Thread:
    def __init__(self, func, fps: int=0):
        self.func = func
        self.fps = fps
        self.thread_on = False
    
    def thread(self):
        if self.fps == 0:
            while True:
                self.func()
        elif self.fps > 0:
            while True:
                self.func()
                time.sleep(1/self.fps)
        else:
            raise ValueError("\"fps\" argument must be above 0")
    
    def start(self):
        self.thread_on = True
        threading.Thread(target=self.thread).start()
    
    def stop(self):
        self.thread_on = False