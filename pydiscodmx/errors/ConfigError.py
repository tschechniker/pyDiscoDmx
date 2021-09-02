from .Error import Error

class ConfigError(Error):
    def __init__(self, message):
        self.message = message