import sys
sys.path.append(".")
import logging
from Cancel.cancel_validator import CancelValidator
from common.util.mapper import CancelMapper
from common.util.service import Service
from Cancel.cancel_activity import CancelActivity

class CancelService(Service):
    def __init__(self, cancel_request):
        booking = CancelMapper().map(cancel_request)
        super().__init__(CancelValidator(booking), 
            CancelActivity(booking.get_booking_id()))