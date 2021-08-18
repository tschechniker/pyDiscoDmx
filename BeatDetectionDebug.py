from btrack import track_beats
from BeatDetectionThread import bpmSignal
import time
import threading

class BeatDetectionDebug:
    def start(self):
        bpmSignal.connect(self.handle)

    def handle(self, sender, **kw):
        print(kw['bpm'])