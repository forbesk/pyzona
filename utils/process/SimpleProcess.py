from multiprocessing import Process, Value
import time

class SimpleProcess(Process):
    def __init__(self, update_period):
        Process.__init__(self)
        self.joined = Value('b', False, lock=False)
        self.ready = Value('b', False, lock=False)
        self.update_period = update_period
        self.last_run_time = time.time()

    def join(self, timeout=1.0):
        self.joined.value = True
        super(SimpleProcess, self).join(timeout)

    def run(self):
        self.setup()
        self.ready.value = True

        while not self.joined.value:
            self.loop()
            sleeptime = self.last_run_time + self.update_period - time.time()
            if sleeptime > 0:
                time.sleep(sleeptime)
            self.last_run_time += self.update_period

        self.close()

    def setup(self):
        pass

    def loop(self):
        pass

    def close(self):
        pass
