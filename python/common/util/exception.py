class NoRefundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoDebitException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoBookingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoCreditCardError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)