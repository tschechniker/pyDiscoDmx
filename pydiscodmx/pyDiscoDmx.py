#!/bin/python3

from .BeatDetectionThread import BeatDetectionThread
from .BeatDetectionDebug import BeatDetectionDebug
from PyDMXControl.controllers import uDMXController
from .EffectHandler import EffectHandler
from queue import Queue
import os
import time

import configparser

def main():
    globalConfig = configparser.ConfigParser()
    globalConfig.read("/etc/pydiscodmx/pyDiscoDmx.ini")

    dmx = uDMXController()
    dmx.json.load_config(globalConfig['dmx']['fixturesConfig'])

    effectHandler = EffectHandler(globalConfig['effects'], dmx)

    beatThread = BeatDetectionThread()
    beatThread.start()

    debug = BeatDetectionDebug()
    if bool(globalConfig['dmx']['debug']):
        debug.start()

    # @ToDo: Make this dynamic
    effectHandler.start("color")

    dmx.sleep_till_interrupt()

    beatThread.stop()
    dmx.close()

if __name__ == '__main__':
    main()
