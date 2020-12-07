import sys
sys.path.append(".")
import logging
from common.util.task import Task
from common.util.booking_type import GetClass
from common.util.transaction import Transaction
from common.util.exception import NoRefundException, NoBookingError

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


class GetCreditDetailsTask(Task):
    def __init__(self, card_no, booking_status):
        self._card_no = card_no
        self._booking_status = booking_status

    def is_confirmed_booking(self):
        return self._booking_status == 'CONFIRMED'

    def perform_activity(self):
        logging.info('perform activity')
        if self.is_confirmed_booking() == False:
            logging.warning(
                'Credit Task: Booking is not Confirmed. No refund Applicable')
            raise NoRefundException('Booking is not Confirmed. No refund Applicable')
        try:
            transaction = Transaction()
            logging.info('GetCreditDetails Task: Selecting credit card details')
            record = transaction.execute(
                "SELECT * FROM CREDIT_CARD_TABLE WHERE card_number={}".format(self._card_no))
            logging.info('Credit Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info('Credit Task: logged response: {}'.format(record))
            if transaction.get_cursor().rowcount < 1:
                raise TypeError('credit card {} is invalid'.format(
                    self._card_no))
            return record
        finally:
            transaction.close()


class UpdateCreditTask(Task):
    def __init__(self, credit_card, flight_class):
        self._credit_card = credit_card
        self._flight_class = flight_class

    def calculate_credit_amount(self):
        associated_class = GetClass(self._flight_class).get_class()
        return associated_class.get_amount() * associated_class.refund_percent()

    def perform_activity(self):
        try:
            amount = self.calculate_credit_amount()
            logging.info('UpdateCredit Task: crediting Amount : {} to ccn {}'.format(
                amount, self._credit_card.get_card_number()))
            transaction = Transaction()
            record = transaction.execute(
                "UPDATE CREDIT_CARD_TABLE SET balance = balance + %s WHERE card_number=%s", 
                (int(amount), self._credit_card.get_card_number()))
            logging.info('UpdateCredit Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info('UpdateCredit Task: logged response: {}'.format(record))
            return 'Rs.{} refunded.'.format(amount)
        finally:
            transaction.close()

    
class GetNumberOfPassengerTask(Task):
    def __init__(self, flight_id):
        self._flight_id = flight_id

    def perform_activity(self):
        try:
            logging.info('GetNumberOfPassenger Task: {}'.format(self._flight_id))
            transaction = Transaction()
            record = transaction.execute(
                "SELECT count(*) FROM BOOKING_TABLE WHERE flight_id="+str(self._flight_id))
            logging.info('GetNumberOfPassenger Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info('GetNumberOfPassenger Task: logged response: {}'.format(record))
            return record[0]
        finally:
            transaction.close()


class RemoveScheduleTask(Task):
    def __init__(self, flight_id):
        self._flight_id = flight_id

    def perform_activity(self):
        try:
            logging.info('UpdateSchedule Task: {}'.format(self._flight_id))
            transaction = Transaction()
            record = transaction.execute(
                "DELETE FROM SCHEDULE_TABLE WHERE flight_id="+str(self._flight_id))
            logging.info('UpdateSchedule Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info('UpdateSchedule Task: logged response: {}'.format(record))
        finally:
            transaction.close()


class RemoveBookingTask(Task):
    def __init__(self, booking_id):
        self._booking_id = booking_id

    def perform_activity(self):
        try:
            logging.info('RemoveBooking Task: {}'.format(self._booking_id))
            transaction = Transaction()
            record = transaction.execute(
                "DELETE FROM BOOKING_TABLE WHERE booking_id="+self._booking_id)
            logging.info('RemoveBooking Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info('RemoveBooking Task: logged response: {}'.format(record))
            return "Flight with bookingid {} canceled.".format(self._booking_id)
        finally:
            transaction.close()