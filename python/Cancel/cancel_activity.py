import sys
sys.path.append(".")
import logging
from common.util.activity import Activity
from common.util.card import CreditCard
from common.util.mapper import BookingTableMapper, CreditCardMapper
from common.util.exception import NoRefundException, NoBookingError
from Cancel.cancel_task import CheckBookingTask, GetCreditDetailsTask, UpdateCreditTask, GetNumberOfPassengerTask, RemoveScheduleTask, RemoveBookingTask

class CancelActivity(Activity):
    def __init__(self, booking_id):
        self._booking_id = booking_id
        self._check_booking_task = None
        self._get_credit_task = None
        self._update_credit_task = None
        self._get_passenger_count_task = None
        self._remove_schedule_task = None
        self._remove_passenger_task = None

    def check_activity(self, booking_id):
        self._check_booking_task = CheckBookingTask(booking_id)
        try:
            return self._check_booking_task.perform_activity()
        except NoBookingError as nbe:
            self.set_error_msg(nbe.message)
            logging.error('PaymentSchedule Activity: check_activity {}'.format(
                self.get_error_msg()))
            raise nbe
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Check Activity: {}'.format(self.get_error_msg()))
            raise TypeError(e)

    def get_credit_activity(self, card_no, booking_status):
        self._get_credit_task = GetCreditDetailsTask(card_no, booking_status)
        try:
            return self._get_credit_task.perform_activity()
        except NoRefundException as ne:
            logging.error('Get Activity: {}'.format(ne))
            raise NoRefundException(ne)
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Get Activity: {}'.format(self.get_error_msg()))
            raise TypeError(e)
    
    def update_activity(self, card_details, flight_class):
        self._update_credit_task = UpdateCreditTask(card_details, flight_class)
        try:
            return self._update_credit_task.perform_activity()
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Update Activity: {}'.format(self.get_error_msg()))
            raise TypeError(e)
    
    def passenger_count_activity(self, flight_id):
        self._get_passenger_count_task = GetNumberOfPassengerTask(flight_id)
        try:
            return self._get_passenger_count_task.perform_activity()
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Get Passenger Count Activity: {}'.format(self.get_error_msg()))
            raise TypeError(e)

    def remove_schedule_activity(self, flight_id):
        self._remove_schedule_task = RemoveScheduleTask(flight_id)
        try:
            return self._remove_schedule_task.perform_activity()
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Update Schedule Activity: {}'.format(self.get_error_msg()))
            raise TypeError(e)
    
    def remove_passenger_activity(self, booking_id):
        self._remove_passenger_task = RemoveBookingTask(booking_id)
        try:
            return self._remove_passenger_task.perform_activity()
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Remove Booking Activity: {}'.format(self.get_error_msg()))
            raise TypeError(e)

    def do(self):
        booking_table = BookingTableMapper().map(self.check_activity(self._booking_id))
        refund_msg = ''
        try:
            credit_card = CreditCardMapper().map(self.get_credit_activity(booking_table.get_card_no(),
            booking_table.get_booking_status()))
            refund_msg = self.update_activity(credit_card, booking_table.get_flight_class())
        except NoRefundException as ne:
            logging.info(ne)
        try:
            count = self.passenger_count_activity(booking_table.get_flight_id())
            if int(count) == 1:
                self.remove_schedule_activity(booking_table.get_flight_id())
        except TypeError as e:
            logging.info(e)
        return self.remove_passenger_activity(self._booking_id) + refund_msg
        