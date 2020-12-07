import sys
sys.path.append(".")
import logging
from common.util.booking import Booking
from common.util.field_validator import BookingIDValidator
from common.util.service_validator import ServiceValidator

class CancelValidator(ServiceValidator):
    def __init__(self, booking):
        self._error_msg = None
        self._booking = booking

    def validate(self):
        bookingidValidator = BookingIDValidator(self._booking.get_booking_id())
        if bookingidValidator.validate() == False:
            logging.warning('Cancel Validator : {}'.format(self._booking.get_booking_id()))
            self._error_msg = bookingidValidator.get_error_msg()
            return False
        return True
    
    def get_error_msg(self):
        return self._error_msg

