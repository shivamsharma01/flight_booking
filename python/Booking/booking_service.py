from Booking.booking_validator import BookingValidator
from common.util.service import Service
from common.util.mapper import BookMapper
from Booking.booking_activity import BookingScheduleActivity
import sys
sys.path.append(".")


class BookingService(Service):
    def __init__(self, booking_request):
        booking = BookMapper().map(booking_request)
        super().__init__(BookingValidator(booking),
                         BookingScheduleActivity(booking))
