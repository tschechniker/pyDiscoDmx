from btrack import track_beats
from PyDMXControl import Colors
import time
import random
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
        self.currentColor = None
        bpmSignal.connect(self.handleTick)

    def handleTick(self, sender, **kw):
        switcher = {
            "manual": self.handleManual,
            "color": self.handleColor
        }
        switcher.get(self.config['META']['type'])(kw)

    def handleManual(self, kw):
        bpm = kw['bpm']
        if (self.currentStep + 1) > self.maxSteps:
            self.currentStep = 1
        else: 
            self.currentStep += 1
        print(self.currentStep)
        stepDict = dict(self.config.items(str(self.currentStep)))
        for key in stepDict:
            fixture = self.dmx.get_fixtures_by_name(key)[0]
            if isinstance(stepDict[key], int):
                fixture.dim(int(stepDict[key]), int(self.config['META']['dimTime']))
            else:
                fixture.color(stepDict[key])

    def getRandomColor(self, current):
        colorList = list(Colors)
        # Delte Black
        del colorList[0]
        # Delte Whote
        del colorList[0]
        newRandColor=random.choice(colorList)
        if (current is not None) and (newRandColor is current):
            return self.getRandomColor(current)
        return newRandColor
    
    def handleColor(self, kw):
        for fixtureName in self.config['META']['fixtures'].split(','):
            fixture = self.dmx.get_fixtures_by_name(fixtureName)[0]
            newColor=self.getRandomColor(self.currentColor)
            self.currentColor = newColor
            fixture.color(newColor)

    def stop(self):
        bpmSignal.disconnect(self.handleTick)
        stepDict = dict(self.config.items(str(self.currentStep)))
        for key in stepDict:
            fixture = self.dmx.get_fixtures_by_name(key)[0]
            fixture.dim(0)