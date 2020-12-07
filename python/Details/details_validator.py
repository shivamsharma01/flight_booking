import sys
sys.path.append(".")
import logging
from common.util.field_validator import BookingIDValidator
from common.util.service_validator import ServiceValidator

class DetailsValidator(ServiceValidator):
    def __init__(self, booking_id):
        self._error_msg = None
        self._booking_id = booking_id

    def validate(self):
        bookingIDValidator = BookingIDValidator(self._booking_id)
        if bookingIDValidator.validate() == False:
            logging.warning('Details Validator: BookingID Validator: {}'.format(self._booking_id))
            self._error_msg = bookingIDValidator.get_error_msg()
            return False
        return True
    
    def get_error_msg(self):
        return self._error_msg
