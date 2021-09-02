from ..Effect import Effect
from PyDMXControl import Colors
import random

class ColorChaseEffect(Effect):
    def __init__(self, config, dmx):
        super().__init__(config, dmx)
        self.fixtures = self.config['META']['fixtures'].split(',')
        if 'mode' in self.config['EFFECT']:
            self.tickMethod = getattr(self, self.config['EFFECT']['mode'])
        else:
            self.tickMethod = self.allSame
        
        self.colorList = list(Colors)
        # Delete Black
        del self.colorList[0]
        # Delete White
        del self.colorList[0]

    def reset(self):
        self.currentColor = None
        self.currentFixtureIndex = 0

    def handleTick(self, sender, **kw):
        self.tickMethod(kw)

    def allSame(self, kw):
        newColor=self.getRandomColor(self.currentColor)
        self.currentColor = newColor
        for fixtureName in self.fixtures:
            fixture = self.getFixture(fixtureName)
            fixture.color(newColor)

    def scroll(self, kw):
        if not hasattr(self, 'scrolls'):
            self.scrolls = []
            prevColor = None
            for fixtureName in self.fixtures:
                color = self.getRandomColor(prevColor)
                self.scrolls.append(color)
                prevColor = color
        else:
            i = len(self.scrolls)
            while i > 0:
                i -= 1
                if i is 0:
                    newColor = self.getRandomColor(self.scrolls[i])
                    self.scrolls[i] = newColor
                else:
                    self.scrolls[i] = self.scrolls[i-1]

        currentFixtureIndex=0
        for fixtureName in self.fixtures:
            fixture = self.getFixture(fixtureName)
            fixture.color(self.scrolls[currentFixtureIndex])
            currentFixtureIndex += 1

    def getRandomColor(self, current):
        newRandColor=random.choice(self.colorList)
        if (current is not None) and (newRandColor is current):
            return self.getRandomColor(current)
        return newRandColor