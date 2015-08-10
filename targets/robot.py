import time
import logging
from utils.process.SimpleProcess import SimpleProcess

class Robot(SimpleProcess):
    def __init__(self, update_period):
        SimpleProcess.__init__(self, update_period)
        self.name = "Robot"

    def setup(self):
        logging.info("Setting up process")

    def loop(self):
        pass

    def close(self):
        logging.info("Closing process")
