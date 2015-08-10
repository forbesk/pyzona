import sys
import os
import logging
from multiprocessing import Process, Manager
import json
import time
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
           'agent': Agent,
           'robot': Robot,
           'sim': Simulator }


def start_process(process):
    logging.info("Starting " + process)
    if process not in processes:
        processes[process] = classes[process](config[process]['loop period'])
        processes[process].start()
    else:
        logging.warn("Process '" + process + "' is already running")

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

    logging.info("Loading model")
    model = manager.dict()
    model['config'] = config
    start_process('model')
    while not processes['model'].ready:
        time.sleep(0.01)
    model = processes['model'].model
    logging.info("Model created")

    time.sleep(0.25)

    logging.info("Loading targets")
    if config['target'] == 'robot':
        start_process('robot')
    elif config['target'] == 'sim':
        start_process('sim')
    else:
        logging.warn("Target ('robot'/'sim') not found")

    time.sleep(0.25)

    logging.info("Loading agent")
    start_process('agent')
    while not processes['agent'].ready:
        time.sleep(0.01)
    logging.info("Agent created")

    logging.info("Sleeping for 5 seconds...")
    time.sleep(5.0)

    kill_all_processes()
