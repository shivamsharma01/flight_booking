import logging
from common.util.task import Task
from common.util.transaction import Transaction
from common.util.exception import NoBookingError, NoCreditCardError
from common.util.booking_type import GetClass

class CheckBookingTask(Task):
    def __init__(self, booking_id):
        self._booking_id = booking_id

    def perform_activity(self):
        try:
            logging.info(
                'CheckBooking Task: checking given booking id: {}'.format(self._booking_id))
            transaction = Transaction()
            record = transaction.execute(
                "SELECT * FROM BOOKING_TABLE WHERE booking_id="+str(self._booking_id))
            logging.info('CheckBooking Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info(
                'CheckBooking Task: logged response: {}'.format(record))
            if transaction.get_cursor().rowcount < 1:
                raise NoBookingError(
                    'No reservation Available. Please check the booking id {}'.format(self._booking_id))
            return record
        finally:
            transaction.close()

class PaymentTask(Task):
    def __init__(self, card_no, flight_class):
        self._card_no = card_no
        self._flight_class = flight_class

    def calculate_debit_amount(self):
        return GetClass(self._flight_class).get_class().get_amount()

    def perform_activity(self):
        logging.info('Payment Task: make payment')
        try:
            transaction = Transaction()
            amount = self.calculate_debit_amount()
            logging.info('Payment Task: debiting Amount : {} from ccn {}'.format(
                amount, self._card_no))
            record = transaction.execute(
                "UPDATE CREDIT_CARD_TABLE SET balance = balance - %s WHERE card_number=%s", 
                (amount, self._card_no))
            logging.info('Payment Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            if transaction.get_cursor().rowcount < 1:
                raise NoCreditCardError(
                    'Credit Card Number {} is not valid.'.format(self._card_no))
            return 'Rs.{} debited.'.format(amount)
        finally:
            transaction.close()

class ConfirmBookingTask(Task):
    def __init__(self, booking_id, card_no):
        self._booking_id = booking_id
        self._card_no = card_no

    def perform_activity(self):
        logging.info('ConfirmBooking Task: confirm booking')
        try:
            transaction = Transaction()
            transaction.execute(
                "UPDATE BOOKING_TABLE SET booking_status=%s, payment_method=%s, card_number=%s WHERE booking_id=%s", 
                 ("CONFIRMED", "CREDIT_CARD", self._card_no, self._booking_id))
            logging.info('ConfirmBooking Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            return 'Booking id {} is confirmed.'.format(self._booking_id)
        finally:
            transaction.close()

