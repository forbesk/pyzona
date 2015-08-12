import sys
import os
import logging
import json
import time
from multiprocessing import Process, Manager
from server.server import Server
from targets.robot import Robot
from targets.simulator import Simulator
from model.model import Model
from agent.agent import Agent

greeting = """
     /\  | |  | \ \    / / |  | |  /\\
    /  \ | |  | |\ \  / /| |  | | /  \\
   / /\ \| |  | | \ \/ / | |  | |/ /\ \\
  / ____ \ |__| |  \  /  | |__| / ____ \\
 /_/    \_\____/    \/    \____/_/    \_\\
 Autonomous Underwater Vehicle
                    University of Arizona

"""

classes = {'model': Model,
           'server': Server,
           'agent': Agent,
           'robot': Robot,
           'sim': Simulator }


def start_process(process, model):
    logging.info("Starting " + process)
    if process not in processes:
        processes[process] = classes[process](config[process]['loop period'],
                                                model)
        processes[process].start()
    else:
        logging.warn("Process '" + process + "' is already running")
    while not processes[process].ready:
        time.sleep(0.01)

def kill_all_processes():
    for key,value in processes.iteritems():
        logging.info("Stopping process '" + value.name + "'")
        value.join()
        processes[key] = None


if __name__=='__main__':
    config = ""
    processes = dict()
    manager = Manager()

    try:
        config_file = open('config.json', 'r')
        config = config_file.read()
        config_file.close()
    except IOError:
        print "Configuration file not found, exiting"
        exit(-1)
    config = json.loads(config)

    model = manager.dict()
    model['config'] = config

    logformat = config['logging']['format']
    filelogger = logging.FileHandler('{0}/{1}.{2}'.format(
        config['logging']['folder'],
        str(time.asctime()),
        config['logging']['extension']).replace(' ', '-'))
    filelogger.setFormatter(logging.Formatter(logformat))
    consolelogger = logging.StreamHandler(sys.stdout)
    consolelogger.setFormatter(logging.Formatter(logformat))
    logging.getLogger().addHandler(filelogger)
    logging.getLogger().addHandler(consolelogger)
    logging.getLogger().setLevel(logging.DEBUG)

    for line in iter(greeting.splitlines()):
        logging.info(line)
    logging.info("Configuration loaded")
    logging.info("Logging to " + filelogger.baseFilename)

    start_process('model', model)
    start_process('server', model)

    if config['target'] == 'robot' or config['target'] == 'sim':
        start_process(config['target'], model)
    else:
        logging.warn("Target ('robot'/'sim') not found")

    logging.info("Loading agent")
    start_process('agent', model)
    logging.info("Agent created")

    logging.info("Sleeping for 60 seconds...")
    time.sleep(60.0)

    kill_all_processes()
