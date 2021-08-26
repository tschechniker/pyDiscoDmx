from .BeatDetectionThread import bpmSignal

class BeatDetectionDebug:
    def start(self):
        bpmSignal.connect(self.handle)

    def handle(self, sender, **kw):
        print(kw['bpm'])