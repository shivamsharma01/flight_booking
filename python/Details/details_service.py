from Details.details_validator import DetailsValidator
from common.util.service import Service
from common.util.mapper import DeatilsMapper
from Details.details_activity import DetailsActivity
import sys
sys.path.append(".")

class DetailsService(Service):
    def __init__(self, details_request):
        booking_id = DeatilsMapper().map(details_request)
        super().__init__(DetailsValidator(booking_id), DetailsActivity(booking_id))
