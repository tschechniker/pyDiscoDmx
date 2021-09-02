from .Effect import Effect
import importlib
import os
import configparser

class EffectHandler:
    effects={}

    def __init__(self, config, dmx):
        self.config = config
        self.dmx = dmx
        self.loadEffects()

    def loadEffects(self):
        for filename in os.listdir(self.config['effectsDir']):
            if filename.endswith(".effect"):
                effectName = filename.replace('.effect', '')
                effectConfig = configparser.ConfigParser()
                effectConfig.read(os.path.join(self.config['effectsDir'], filename))
                effectModuleName = effectConfig['EFFECT']['module']
                effectClassName = effectConfig['EFFECT']['class']
                EffectClass = getattr(importlib.import_module(effectModuleName), effectClassName)
                if not issubclass(EffectClass, Effect):
                    print(EffectClass.__name__ + " is not a subclass of Effect. Skipping!")
                    continue
                self.effects[effectName] = EffectClass(effectConfig, self.dmx)
            else:
                continue
    
    def start(self, effectName):
        self.effects[effectName].start()

    def stop(self, effectName):
        self.effects[effectName].stop()