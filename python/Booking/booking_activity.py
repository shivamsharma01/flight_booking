import logging
from common.util.activity import Activity
from Booking.booking_task import CheckScheduleTask, AddScheduleTask, GetScheduleTask, AddBookingTask

class BookingScheduleActivity(Activity):
    def __init__(self, booking):
        self._booking = booking
        self._checker = None
        self._adder = None
        self._getter = None
        self._add_booking = None

    def check_schedule(self, source, destination, date):
        self._checker = CheckScheduleTask(source, destination, date)
        try:
            return self._checker.perform_activity()
        except:
            self.set_error_msg('Internal error while checking flight status')
            logging.error('Schedule Activity: check_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def add_schedule(self, source, destination, date):
        self._adder = AddScheduleTask(source, destination, date)
        try:
            self._adder.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while adding new flight schedule')
            logging.error('Schedule Activity: add_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def get_schedule(self, source, destination, date):
        self._getter = GetScheduleTask(source, destination, date)
        try:
            return self._getter.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while adding get flight schedule')
            logging.error('Schedule Activity: get_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def add_booking(self, booking, flight_id):
        self._add_booking = AddBookingTask(booking, flight_id)
        try:
            return self._add_booking.perform_activity()
        except:
            self.set_error_msg('Internal error while adding the new passenger')
            logging.error('Schedule Activity: add_booking {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def do(self):
        if self.check_schedule(self._booking.get_src_location(), self._booking.get_dest_location(), self._booking.get_travel_date()) == False:
            self.add_schedule(self._booking.get_src_location(), self._booking.get_dest_location(), self._booking.get_travel_date())
        flight_id = self.get_schedule(self._booking.get_src_location(), self._booking.get_dest_location(), self._booking.get_travel_date())
        return self.add_booking(self._booking, flight_id)
