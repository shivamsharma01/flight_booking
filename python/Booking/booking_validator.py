import sys
sys.path.append(".")
import logging
from common.util.field_validator import NameValidator, PastDateValidator, PlaceValidator, FlightClassValidator
from common.util.service_validator import ServiceValidator

class BookingValidator(ServiceValidator):
    def __init__(self, booking):
        self._error_msg = None
        self._booking = booking

    def validate(self):
        nameValidator = NameValidator(self._booking.get_name())
        if nameValidator.validate() == False:
            logging.warning('Booking Validator: Invalid name sent: {}'.format(self._booking.get_name()))
            self._error_msg = nameValidator.get_error_msg()
            return False
        pastdateValidator = PastDateValidator(self._booking.get_travel_date())
        if pastdateValidator.validate() == True:
            logging.warning('Booking Validator: Past Date sent: {}'.format(self._booking.get_travel_date()))
            self._error_msg = pastdateValidator.get_error_msg()
            return False
        sourceValidator = PlaceValidator(self._booking.get_src_location(), True)
        if sourceValidator.validate() == False:
            logging.warning('Booking Validator: Invalid source location sent: {}'.format(self._booking.get_src_location()))
            self._error_msg = sourceValidator.get_error_msg()
            return False
        destinationValidator = PlaceValidator(self._booking.get_dest_location(), False)
        if destinationValidator.validate() == False:
            logging.warning('Booking Validator: Invalid destination location sent: {}'.format(self._booking.get_dest_location()))
            self._error_msg = destinationValidator.get_error_msg()
            return False
        classValidator = FlightClassValidator(self._booking.get_flight_class())
        if classValidator.validate() == False:
            logging.warning('Booking Validator: Invalid class set: {}'.format(self._booking.get_flight_class()))
            self._error_msg = classValidator.get_error_msg()
            return False
        return True
    
    def get_error_msg(self):
        return self._error_msg
