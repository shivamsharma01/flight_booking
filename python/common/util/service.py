class Service:
    def __init__(self, validator, activity):
        self._validator = validator
        self._activity = activity

    def get_validator(self):
        return self._validator

    def get_activity(self):
        return self._activity
