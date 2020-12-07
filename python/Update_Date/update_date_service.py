from Update_Date.update_date_validator import UpdateDateValidator
from common.util.service import Service
from common.util.mapper import UpdateDateMapper
from Update_Date.update_date_activity import UpdateDateActivity
import sys
sys.path.append(".")


class UpdateDateService(Service):
    def __init__(self, booking_request):
        booking = UpdateDateMapper().map(booking_request)
        super().__init__(UpdateDateValidator(
            booking.get_booking_id(), booking.get_travel_date()), 
            UpdateDateActivity(
            booking.get_booking_id(), booking.get_travel_date()))