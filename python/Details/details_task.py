import logging
from common.util.task import Task
from common.util.transaction import Transaction
from common.util.exception import NoBookingError

class DetailsTask(Task):
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
