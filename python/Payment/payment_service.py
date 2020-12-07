from Payment.payment_validator import PaymentValidator
from common.util.service import Service
from common.util.mapper import PaymentMapper
from Payment.payment_activity import PaymentScheduleActivity
import sys
sys.path.append(".")


class PaymentService(Service):
    def __init__(self, booking_request):
        booking = PaymentMapper().map(booking_request)
        super().__init__(PaymentValidator(booking),
                         PaymentScheduleActivity(booking))
