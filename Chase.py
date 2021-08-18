from btrack import track_beats
import time
from BeatDetectionThread import bpmSignal

class Chase():
    def __init__(self, config, dmx):
        self.config = config
        self.maxSteps = len(config.sections()) -1
        self.dmx = dmx
        

    def capableOfBpm(self, bpm):
        return bpm > float(self.config['META']['bpmMin']) and bpm < float(self.config['META']['bpmMax'])
    
    def start(self):
        self.currentStep = 0
        bpmSignal.connect(self.handleTick)

    def handleTick(self, sender, **kw):
            bpm = kw['bpm']
            if (self.currentStep + 1) > self.maxSteps:
                self.currentStep = 1
            else: 
                self.currentStep += 1
            print(self.currentStep)
            stepDict = dict(self.config.items(str(self.currentStep)))
            for key in stepDict:
                fixture = self.dmx.get_fixtures_by_name(key)[0]
                fixture.dim(int(stepDict[key]), int(self.config['META']['dimTime']))

    def stop(self):
        bpmSignal.disconnect(self.handleTick)
        stepDict = dict(self.config.items(str(self.currentStep)))
        for key in stepDict:
            fixture = self.dmx.get_fixtures_by_name(key)[0]
            fixture.dim(0)