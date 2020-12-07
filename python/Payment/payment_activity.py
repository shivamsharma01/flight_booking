import logging
from common.util.activity import Activity
from common.util.exception import NoDebitException, NoBookingError, NoCreditCardError
from common.util.mapper import BookingTableMapper
from Payment.payment_task import CheckBookingTask, ConfirmBookingTask, PaymentTask

class PaymentScheduleActivity(Activity):
    def __init__(self, book):
        self._book = book
        self._checker = None
        self._payment = None
        self._booking = None

    def is_confirmed_booking(self, status):
        return status == 'CONFIRMED'

    def check_activity(self, booking_id):
        self._checker = CheckBookingTask(booking_id)
        try:
            return self._checker.perform_activity()
        except NoBookingError as nbe:
            self.set_error_msg(nbe.message)
            logging.error('PaymentSchedule Activity: check_activity {}'.format(
                self.get_error_msg()))
            raise nbe
        except:
            self.set_error_msg('Internal error while checking booking status')
            logging.error('PaymentSchedule Activity: check_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())
    
    def payment_activity(self, card_no, flight_class):
        self._payment = PaymentTask(card_no, flight_class)
        try:
            return self._payment.perform_activity()
        except NoCreditCardError as nce:
            self.set_error_msg(nce.message)
            logging.error('PaymentSchedule Activity: payment_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())
        except:
            self.set_error_msg(
                'Internal error while making payment')
            logging.error('PaymentSchedule Activity: payment_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())
    
    def confirm_booking_activity(self, booking_id, card_no):
        self._booking = ConfirmBookingTask(booking_id, card_no)
        try:
            return self._booking.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while confirming booking')
            logging.error('PaymentSchedule Activity: confirm_booking_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def do(self):
        booking_table = BookingTableMapper().map(self.check_activity(self._book.get_booking_id()))        
        if self.is_confirmed_booking(booking_table.get_booking_status()) == True:
            self.set_error_msg('This booking is already confirmed!!!')
            raise NoDebitException(self.get_error_msg())
        debit_msg = self.payment_activity(self._book.get_card_no(), booking_table.get_flight_class())
        return self.confirm_booking_activity(self._book.get_booking_id(), self._book.get_card_no()) + debit_msg
