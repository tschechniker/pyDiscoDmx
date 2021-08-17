class chase:
    config=None
    currentStep=1
    maxSteps=None
    def __init__(self, config):
        self.config = config
        self.maxSteps = len(config.sections()) -1

    def capableOfBpm(self, bpm):
        return bpm > self.config['META']['bpmMin'] and bpm < self.config['META']['bpmMax']
    
    def nextStep(self, dmx, bpm):
        if (self.currentStep + 1) > self.maxSteps:
            self.currentStep = 1
        else: 
            self.currentStep += 1
        stepDict = dict(self.config.items(str(self.currentStep)))
        for key in stepDict:
            fixture = dmx.get_fixtures_by_name(key)[0]
            fixture.dim(int(stepDict[key]))