import logging
from common.util.activity import Activity
from Booking.booking_task import CheckScheduleTask, AddScheduleTask, GetScheduleTask, AddBookingTask

class BookingScheduleActivity(Activity):
    def __init__(self, booking):
        self._booking = booking
        self._check_schedule_task = None
        self._add_schedule_task = None
        self._get_schedule_task = None
        self._add_booking_task = None

    def check_schedule(self, source, destination, date):
        self._check_schedule_task = CheckScheduleTask(source, destination, date)
        try:
            return self._check_schedule_task.perform_activity()
        except:
            self.set_error_msg('Internal error while checking flight status')
            logging.error('Schedule Activity: check_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def add_schedule(self, source, destination, date):
        self._add_schedule_task = AddScheduleTask(source, destination, date)
        try:
            self._add_schedule_task.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while adding new flight schedule')
            logging.error('Schedule Activity: add_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def get_schedule(self, source, destination, date):
        self._get_schedule_task = GetScheduleTask(source, destination, date)
        try:
            return self._get_schedule_task.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while adding get flight schedule')
            logging.error('Schedule Activity: get_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def add_booking(self, booking, flight_id):
        self._add_booking_task = AddBookingTask(booking, flight_id)
        try:
            return self._add_booking_task.perform_activity()
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
