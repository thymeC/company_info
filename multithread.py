import threading
import time


class multiThreadingRun(threading.Thread):
    def __init__(self, threadName, func, *args):
        threading.Thread.__init__(self)
        self._func = func
        self._args = args
        self.threadName = threadName

    def run(self):
        print("Starting " + self.threadName)
        self.result = self._func(*self._args)
        print("Exiting " + self.threadName)

    def get_result(self):
        threading.Thread.join(self)
        try:
            return self.result
        except Exception:
            return None