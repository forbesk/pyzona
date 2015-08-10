import logging
from utils.process.SimpleProcess import SimpleProcess

class Model(SimpleProcess):
    def __init__(self, model, update_period=0.02):
        SimpleProcess.__init__(self, update_period)
        self.name = "Model"
        self.model = model

    def setup(self):
        logging.info("Setting up process")

    def loop(self):
        pass

    def close(self):
        logging.info("Closing process")
