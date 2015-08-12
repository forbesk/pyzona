import os
import time
import logging
from utils.process.SimpleProcess import SimpleProcess
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class Server(SimpleProcess):
    def __init__(self, update_period, model):
        SimpleProcess.__init__(self, update_period)
        self.model = model
        self.name = "Server"

    def setup(self):
        logging.info("Setting up process")
        server = self.model['config']['server']
        path = os.getcwd() + '/'
        try:
            os.chdir(path + server['relative_dir'])
            serveraddr = (server['address'], server['port'])
            RedirectedHTTPServer.protocol_version = "HTTP/1.0"
            self.http = BaseHTTPServer.HTTPServer(serveraddr, RedirectedHTTPServer)
            self.http.timeout = self.update_period / 2.0
            logging.info("Server running at %s:%i" %
                    (server['address'], server['port']))
        except Exception as e:
            logging.critical("Error starting server:")
            logging.critical(str(e))
            self.http = None
        finally:
            os.chdir(path)

    def loop(self):
        if not self.http:
            logging.critical("Server did not start, exiting process")
            self.joined.value = True
        else:
            """ This is pretty ugly... """
            path = os.getcwd()
            os.chdir(path + '/' + self.model['config']['server']['relative_dir'])
            self.http.handle_request()
            os.chdir(path)

    def close(self):
        logging.info("Closing process")


class RedirectedHTTPServer(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info("%s - - [%s] %s" %
                     (self.address_string(),
                      self.log_date_time_string(),
                      format%args))
