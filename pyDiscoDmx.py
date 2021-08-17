#!/bin/python3

from PyDMXControl.controllers import uDMXController
from PyDMXControl.profiles.Generic import Dimmer
from btrack import track_beats
import time
from queue import Queue
from threading import Thread

tmp = False

dmx = uDMXController()
fixture = dmx.add_fixture(Dimmer, name="My_First_Dimmer")
fixture2 = dmx.add_fixture(Dimmer, name="My_First_Dimmer", start_channel=4)

def beatDetection(out_q):
    with track_beats() as tracker:
        while True:
            if tracker.has_beats() and tracker.vol > 0.01:
                out_q.put(tracker.bpm)
               # print("Beat (py):", tracker.bpm)
                time.sleep(0.01)

def beatHandler(in_q):
    global tmp
    while True:
        data = in_q.get()
        print(data)
        if tmp:
            fixture.on()
            fixture2.off()
        else:
            fixture.off()
            fixture2.on()
        tmp = not tmp


q = Queue()
t1 = Thread(target = beatHandler, args =(q, ))
t2 = Thread(target = beatDetection, args =(q, ))
t1.start()
t2.start()
