import sys
sys.path.append(".")
import logging
from common.util.field_validator import BookingIDValidator, CreditCardValidator
from common.util.service_validator import ServiceValidator

class AddOnValidator(ServiceValidator):
    def __init__(self, booking):
        self._booking = booking
        self._error_msg = None

    def validate(self):
        bookingIDValidator = BookingIDValidator(self._booking.get_booking_id())
        if bookingIDValidator.validate() == False:
            logging.warning('PaymentValidator: BookingID Validator: {}'.format(self._booking.get_booking_id()))
            self._error_msg = bookingIDValidator.get_error_msg()
            return False
        cardValidator = CreditCardValidator(self._booking.get_card_no())
        if cardValidator.validate() == False:
            logging.warning('PaymentValidator: Card Validator: {}'.format(self._booking.get_card_no()))
            self._error_msg = cardValidator.get_error_msg()
            return False
        return True
    
    def get_error_msg(self):
        return self._error_msg
