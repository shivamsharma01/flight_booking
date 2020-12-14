import logging
from common.util.task import Task
from common.util.transaction import Transaction
from common.util.exception import NoBookingError


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


class CheckScheduleTask(Task):
    def __init__(self, source, destination, date):
        self._source = source
        self._destination = destination
        self._date = date

    def perform_activity(self):
        try:
            logging.info('CheckSchedule Task: checking flight schedule')
            transaction = Transaction()
            status = transaction.execute("select case when count(*) = 1 then 'true' else 'false' end as bool from schedule_table where src_location = %s AND dest_location = %s AND travel_date = %s",
                                         (self._source, self._destination, self._date))[0].lower() == 'true'
            logging.info(
                'CheckSchedule Task: logged response {}'.format(status))
            return status
        finally:
            transaction.close()


class AddScheduleTask(Task):
    def __init__(self, source, destination, date):
        self._source = source
        self._destination = destination
        self._date = date

    def perform_activity(self):
        try:
            logging.info('AddSchedule Task: adding new flight schedule')
            transaction = Transaction()
            transaction.execute('insert into SCHEDULE_TABLE(src_location, dest_location, travel_date) VALUES (%s, %s, %s)',
                                (self._source, self._destination, self._date))
            logging.info('AddSchedule Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            return transaction.execute('SELECT LAST_INSERT_ID()')[0]
        finally:
            transaction.close()


class UpdateBookingTask(Task):
    def __init__(self, booking_id, date, flight_id):
        self._booking_id = booking_id
        self._date = date
        self._flight_id = flight_id
        
    def perform_activity(self):
        try:
            logging.info('UpdateBooking Task: update booking timings.')
            transaction = Transaction()
            transaction.execute('UPDATE BOOKING_TABLE SET flight_id=%s, travel_date=%s WHERE booking_id=%s',
                                (self._flight_id, self._date, self._booking_id))
            logging.info('UpdateBooking Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            return 'Booking {} is now rescheduled to {}. '.format(self._booking_id, self._date)
        finally:
            transaction.close()
