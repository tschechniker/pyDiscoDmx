from btrack import track_beats
from blinker import signal
import time
import threading

bpmSignal = signal('bpm')

class BeatDetectionThread(threading.Thread):
    def __init__(self):
        super(BeatDetectionThread, self).__init__()
        self.stopped=False

    def run(self):
        with track_beats() as tracker:
            while not self.stopped:
                if tracker.has_beats() and tracker.vol > 0.01:
                    bpmSignal.send(self, bpm=tracker.bpm)
                    time.sleep(0.01)

    def stop(self):
        self.stopped = True
        self.join()