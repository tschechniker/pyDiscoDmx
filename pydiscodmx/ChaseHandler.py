from .Chase import Chase
import os
import configparser

class ChaseHandler:
    chases={}

    def __init__(self, config, dmx):
        self.config = config
        self.dmx = dmx
        self.loadChases()

    def loadChases(self):
        for filename in os.listdir(self.config['chasesDir']):
            if filename.endswith(".chase"):
                chaseName = filename.replace('.chase', '')
                chaseConfig = configparser.ConfigParser()
                chaseConfig.read(os.path.join(self.config['chasesDir'], filename))
                self.chases[chaseName] = Chase(chaseConfig, self.dmx)
            else:
                continue
    
    def start(self, chaseName):
        self.chases[chaseName].start()

    def stop(self, chaseName):
        self.chases[chaseName].stop()