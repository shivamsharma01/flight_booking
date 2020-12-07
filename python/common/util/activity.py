class Activity:
    def __init__(self):
        self._error_msg = None

    def set_error_msg(self, msg):
        self._error_msg = msg
    
    def get_error_msg(self):
        return self._error_msg

    def do(self):
        pass
