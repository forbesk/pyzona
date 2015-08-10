import logging
from utils.process.SimpleProcess import SimpleProcess

class Agent(SimpleProcess):
    def __init__(self, update_period):
        SimpleProcess.__init__(self, update_period)
        self.name = "Agent"

    def setup(self):
        logging.info("Setting up process")

    def loop(self):
        pass

    def close(self):
        logging.info("Closing process")
