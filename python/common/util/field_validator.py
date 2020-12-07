import logging
import string
import re
from common.util.dateutility import DateUtility


class FieldValidator:
    def __init__(self, error_msg=None):
        self.error_msg = error_msg

    def validate(self):
        pass

    def get_error_msg(self):
        return self.error_msg


class PastDateValidator(FieldValidator):
    def __init__(self, date):
        super().__init__('Booking cannot be done for a past date')
        self._date = date

    def validate(self):
        logging.info(
            'Booking Validator: Validating Past Date {}'.format(self._date))
        return self._date == '' or DateUtility.is_past_date(self._date)


class NameValidator(FieldValidator):
    def __init__(self, name):
        super().__init__('Please check the name')
        self._name = name

    def validate(self):
        logging.info('Name Validator: Validating name:- {}'.format(self._name))
        return all(c in string.ascii_letters + ' ' for c in self._name) and self._name != ''


class PlaceValidator(FieldValidator):
    def __init__(self, location, isSource=True):
        super().__init__('Please check the {} Location'.format(self.get_tag(isSource)))
        self._location = location
        self._is_source = isSource

    def validate(self):
        logging.info('Place Validator: Validating {}:- {}'.format(
            self.get_tag(self._is_source), self._location))
        return all(c in string.ascii_letters + ' ' for c in self._location) and self._location != ''

    @staticmethod
    def get_tag(source=True):
        if source == True:
            return 'Source'
        else:
            return 'Destination'


class FlightClassValidator(FieldValidator):
    def __init__(self, flight_class):
        super().__init__('Seat Type can be Economy, Business Or First Class')
        self._flight_class = flight_class

    def validate(self):
        logging.info(
            'Flight Class Validator: Validating class:- {}'.format(self._flight_class))
        return self._flight_class in ['E', 'F', 'B']


class PositiveIntegerValidator(FieldValidator):
    def __init__(self, num, msg='Number Should be an Integer greater than 0'):
        super().__init__(msg)
        self._num = str(num)

    def validate(self):
        logging.info(
            'Positive Integer Validator: Validating number:- {}'.format(self._num))
        return bool(re.match("^\d+$", self._num)) == True and int(self._num, base=10) > 0


class BookingIDValidator(PositiveIntegerValidator):
    def __init__(self, booking_id):
        super().__init__(booking_id, 'Booking Id Should be an Integer greater than 0')


class CreditCardValidator(PositiveIntegerValidator):
    def __init__(self, card_no):
        super().__init__(card_no, 'Credit Card Number Should be an Integer greater than 0')


class BalanceValidator(PositiveIntegerValidator):
    def __init__(self, balance):
        super().__init__(balance, 'Balance Should be an Integer greater than 0')
        self._balance = balance

    def validate(self):
        logging.info(
            'Balance Validator: Validating balance:- {}'.format(self._balance))
        return self._balance is None or self._balance == '' or super().validate()
