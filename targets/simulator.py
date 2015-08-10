import time
import logging
from multiprocessing import Process
from utils.process.SimpleProcess import SimpleProcess

class Simulator(SimpleProcess):
    def __init__(self, update_period):
        SimpleProcess.__init__(self, update_period)
        self.name = "Simulator"

    def setup(self):
        logging.info("Setting up process")

    def loop(self):
        pass

    def close(self):
        logging.info("Closing process")
