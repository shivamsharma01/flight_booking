import logging
from common.util.activity import Activity
from common.util.exception import NoBookingError, NoCreditCardError
from common.util.mapper import BookingTableMapper
from Add_On.add_on_task import CheckBookingTask, UpdateCreditTask, UpdateBookingTask


class AddOnActivity(Activity):
    def __init__(self, booking_id, card_no):
        self._booking_id = booking_id
        self._card_no = card_no
        self._checker = None
        self._update_credit = None
        self._update_booking = None

    def is_confirmed_booking(self, status):
        return status == 'CONFIRMED'

    def is_add_on_availed(self, status):
        return status == 'YES'

    def check_activity(self, booking_id):
        self._checker = CheckBookingTask(booking_id)
        try:
            return self._checker.perform_activity()
        except NoBookingError as nbe:
            self.set_error_msg(nbe.message)
            logging.error('AddOn Activity: check_activity {}'.format(
                self.get_error_msg()))
            raise nbe
        except:
            self.set_error_msg('Internal error while checking booking status')
            logging.error('AddOn Activity: check_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def update_credit_activity(self, card_no):
        self._update_credit = UpdateCreditTask(card_no)
        try:
            return self._update_credit.perform_activity()
        except NoCreditCardError as nce:
            self.set_error_msg(nce.message)
            logging.error('AddOn Activity: update_credit_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())
        except:
            self.set_error_msg(
                'Internal error while making payment')
            logging.error('AddOn Activity: update_credit_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def update_booking_activity(self, booking_id):
        self._update_booking = UpdateBookingTask(booking_id)
        try:
            return self._update_booking.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while confirming booking')
            logging.error('AddOn Activity: update_booking_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def do(self):
        booking_table = BookingTableMapper().map(self.check_activity(self._booking_id))
        if self.is_confirmed_booking(booking_table.get_booking_status()) == False:
            self.set_error_msg(
                'Cannot add luggage facility!!! Flight is not confirmed.')
            logging.error('AddOn Activity: do {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())
        if self.is_add_on_availed(booking_table.get_add_on()) == True:
            self.set_error_msg(
                'Luggage Facility Already Availed!!!')
            logging.error('AddOn Activity: do {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())    
        msg = self.update_credit_activity(self._card_no)
        return self.update_booking_activity(self._booking_id) + msg
