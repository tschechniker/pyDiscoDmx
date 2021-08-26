#!/bin/python3

from .BeatDetectionThread import BeatDetectionThread
from .BeatDetectionDebug import BeatDetectionDebug
from PyDMXControl.controllers import uDMXController
from .ChaseHandler import ChaseHandler
from queue import Queue
import os
import time

import configparser

def main():
    globalConfig = configparser.ConfigParser()
    globalConfig.read("/etc/pydiscodmx/pyDiscoDmx.ini")

    dmx = uDMXController()
    dmx.json.load_config(globalConfig['dmx']['fixturesConfig'])

    chaseHandler = ChaseHandler(globalConfig['chases'], dmx)

    beatThread = BeatDetectionThread()
    beatThread.start()

    debug = BeatDetectionDebug()
    if bool(globalConfig['dmx']['debug']):
        debug.start()

    # @ToDo: Make this dynamic
    chaseHandler.start("color")

    dmx.sleep_till_interrupt()

    beatThread.stop()
    dmx.close()

if __name__ == '__main__':
    main()
