from rxfunc import RxFunc
import time

class RxUtils:
    def __init__(self):
        pass

    def __init__(self, rxvar):
        self.rxvar = rxvar
        self.prevvalue = rxvar.value
        self.sum = 0.0
        self.prevtime = time.time()

    def integrate(self):
        self.sum += self.rxvar.get() * (time.time() - self.prevtime)
        self.prevtime = time.time()
        return self.sum

    def differentiate(self):
        diff = (self.rxvar.get() - self.prevvalue)/(time.time() - self.prevtime)
        self.prevtime = time.time()
        self.prevvalue = rxvar.get()
        return diff
