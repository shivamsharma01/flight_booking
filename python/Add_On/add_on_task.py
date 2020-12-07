import logging
from common.util.task import Task
from common.util.transaction import Transaction
from common.util.exception import NoBookingError, NoCreditCardError


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


class UpdateCreditTask(Task):
    def __init__(self, _card_no, amount=500):
        self._card_no = _card_no
        self._amount = amount

    def perform_activity(self):
        try:
            logging.info('UpdateCredit Task: Debiting Amount : {} from ccn {}'.format(
                self._amount, self._card_no))
            transaction = Transaction()
            transaction.execute(
                "UPDATE CREDIT_CARD_TABLE SET balance = balance - %s WHERE card_number=%s", 
                (self._amount, self._card_no))
            logging.info('UpdateCredit Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            if transaction.get_cursor().rowcount < 1:
                raise NoCreditCardError(
                    'Credit Card Number {} is not valid.'.format(self._card_no))
            return 'Rs.{} debited.'.format(self._amount)
        finally:
            transaction.close()


class UpdateBookingTask(Task):
    def __init__(self, booking_id):
        self._booking_id = booking_id

    def perform_activity(self):
        try:
            logging.info('UpdateBooking Task: updating add on status.')
            transaction = Transaction()
            transaction.execute('UPDATE BOOKING_TABLE SET add_on=%s WHERE booking_id=%s',
                                ('YES', self._booking_id))
            logging.info('UpdateBooking Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            return "Congratulations!!! Luggage Facility is updated for booking id {}. ".format(self._booking_id)
        finally:
            transaction.close()
