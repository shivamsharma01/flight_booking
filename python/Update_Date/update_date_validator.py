import sys
sys.path.append(".")
import logging
from common.util.field_validator import BookingIDValidator, PastDateValidator
from common.util.service_validator import ServiceValidator

class UpdateDateValidator(ServiceValidator):
    def __init__(self, booking_id, date):
        self._error_msg = None
        self._booking_id = booking_id
        self._date = date

    def validate(self):
        pastdateValidator = PastDateValidator(self._date)
        if pastdateValidator.validate() == True:
            logging.warning('UpdateDate Validator: Past Date sent: {}'.format(self._date))
            self._error_msg = pastdateValidator.get_error_msg()
            return False
        bookingidValidator = BookingIDValidator(self._booking_id)
        if bookingidValidator.validate() == False:
            logging.warning('Cancel Validator : {}'.format(self._booking_id))
            self._error_msg = bookingidValidator.get_error_msg()
            return False
        return True
    
    def get_error_msg(self):
        return self._error_msg
