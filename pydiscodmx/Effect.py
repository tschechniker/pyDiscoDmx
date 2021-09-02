from abc import ABC, abstractmethod
from .BeatDetectionThread import bpmSignal
from .errors.ConfigError import ConfigError

class Effect(ABC):
    def __init__(self, config, dmx):
        self.config = config
        self.dmx = dmx
    
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def handleTick(self, sender, **kw):
        pass

    def start(self):
        self.reset()
        bpmSignal.connect(self.handleTick)

    def stop(self):
        bpmSignal.disconnect(self.handleTick)

    def getFixture(self, fixtureName):
        try:
            return self.dmx.get_fixtures_by_name(fixtureName)[0]
        except IndexError:
            raise ConfigError(fixtureName + " seems not to be defind in fixtures.json!")