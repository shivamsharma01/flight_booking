import logging
from common.util.task import Task
from common.util.transaction import Transaction


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
        finally:
            transaction.close()


class GetScheduleTask(Task):
    def __init__(self, source, destination, date):
        self._source = source
        self._destination = destination
        self._date = date

    def perform_activity(self):
        try:
            logging.info('GetSchedule Task: get flight schedule')
            transaction = Transaction()
            flight = transaction.execute('SELECT * FROM SCHEDULE_TABLE WHERE src_location=%s AND dest_location=%s AND travel_date=%s',
                                         (self._source, self._destination, self._date))
            logging.info('GetSchedule Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info('GetSchedule Task: log response {}'.format(flight))
            return flight[0]
        finally:
            transaction.close()


class AddBookingTask(Task):
    def __init__(self, booking, flight_id):
        self._booking = booking
        self._flight_id = flight_id

    def perform_activity(self):
        try:
            logging.info('AddBooking Task: add passenger')
            transaction = Transaction()
            flight = transaction.execute('insert into BOOKING_TABLE(name, src_location, dest_location, class, booking_status, payment_method, travel_date, flight_id, add_on) VALUES (%s, %s, %s, %s, "PENDING", "PENDING", %s, %s, "NO")',
                                         (self._booking.get_name(), self._booking.get_src_location(), self._booking.get_dest_location(),
                                          self._booking.get_flight_class(), self._booking.get_travel_date(), self._flight_id))
            logging.info('AddBooking Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            logging.info('AddBooking Task: log response {}'.format(flight))
            logging.info('AddBooking Task: log response {}'.format(
                transaction.get_cursor().lastrowid))
            return transaction.get_cursor().lastrowid
        finally:
            transaction.close()
