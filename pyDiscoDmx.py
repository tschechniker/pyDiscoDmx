#!/bin/python3

from PyDMXControl.controllers import uDMXController
from PyDMXControl.profiles.Generic import Dimmer
from btrack import track_beats
import time
from queue import Queue
from threading import Thread
import configparser
import os
from chase import chase

tmp = False
chases = []
currentChase = None

dmx = uDMXController()
dmx.json.load_config('fixtures.json')

def loadChases():
    for filename in os.listdir("chases"):
        if filename.endswith(".chase"):
            config = configparser.ConfigParser()
            config.read(os.path.join("chases", filename))
            chases.append(chase(config))
        else:
            continue

def beatDetection(out_q):
    with track_beats() as tracker:
        while True:
            if tracker.has_beats() and tracker.vol > 0.01:
                out_q.put(tracker.bpm)
               # print("Beat (py):", tracker.bpm)
                time.sleep(0.01)

def beatHandler(in_q):
    global tmp
    global currentChase
    global chases
    global dmx
    while True:
        data = in_q.get()
        if currentChase == None:
            currentChase = chases[0]
        currentChase.nextStep(dmx, data)

loadChases()
q = Queue()
t1 = Thread(target = beatHandler, args =(q, ))
t2 = Thread(target = beatDetection, args =(q, ))
t1.start()
t2.start()
