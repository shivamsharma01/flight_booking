from Add_On.add_on_validator import AddOnValidator
from common.util.service import Service
from common.util.mapper import AddOnMapper
from Add_On.add_on_activity import AddOnActivity
import sys
sys.path.append(".")


class AddOnService(Service):
    def __init__(self, add_on_request):
        booking = AddOnMapper().map(add_on_request)
        super().__init__(AddOnValidator(booking),
                         AddOnActivity(booking.get_booking_id(), booking.get_card_no()))
