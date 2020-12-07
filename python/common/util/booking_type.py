class DefaultBookingType:
    def __init__(self):
        self._amount = 5000

    def get_amount(self):
        return self._amount

    def refund_percent(self):
        return 0.5

class BusinessClass(DefaultBookingType):
    def __init__(self):
        self._amount = 10000
    
    def refund_percent(self):
        return 0.6

class FirstClass(DefaultBookingType):
    def __init__(self):
        self._amount = 20000
    
    def refund_percent(self):
        return 0.75

class GetClass:
    def __init__(self, flight_class):
        self._flight_class = flight_class

    def get_class(self):
        if self._flight_class == 'F':
            return FirstClass()
        elif self._flight_class == 'B':
            return BusinessClass()
        else:
            return DefaultBookingType()
