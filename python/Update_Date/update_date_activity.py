import logging
from common.util.activity import Activity
from common.util.exception import NoBookingError
from common.util.mapper import BookingTableMapper
from Update_Date.update_date_task import CheckBookingTask, GetNumberOfPassengerTask, RemoveScheduleTask, CheckScheduleTask, AddScheduleTask, UpdateBookingTask


class UpdateDateActivity(Activity):
    def __init__(self, booking_id, date):
        self._booking_id = booking_id
        self._date = date
        self._check_booking_task = None
        self._passenger_count_task = None
        self._remove_schedule_task = None
        self._check_schedule_task = None
        self._add_schedule_task = None
        self._update_booking_task = None

    def is_confirmed_booking(self, status):
        return status == 'CONFIRMED'

    def check_activity(self, booking_id):
        self._check_booking_task = CheckBookingTask(booking_id)
        try:
            return self._check_booking_task.perform_activity()
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

    def passenger_count_activity(self, flight_id):
        self._passenger_count_task = GetNumberOfPassengerTask(flight_id)
        try:
            return self._passenger_count_task.perform_activity()
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Get Passenger Count Activity: {}'.format(
                self.get_error_msg()))
            raise TypeError(e)

    def remove_schedule_activity(self, flight_id):
        self._remove_schedule_task = RemoveScheduleTask(flight_id)
        try:
            return self._remove_schedule_task.perform_activity()
        except TypeError as e:
            self.set_error_msg(e)
            logging.error('Update Schedule Activity: {}'.format(
                self.get_error_msg()))
            raise TypeError(e)

    def check_schedule(self, source, destination, date):
        self._check_schedule_task = CheckScheduleTask(source, destination, date)
        try:
            return self._check_schedule_task.perform_activity()
        except:
            self.set_error_msg('Internal error while checking flight status')
            logging.error('UpdateDate Activity: check_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def add_schedule(self, source, destination, date):
        self._add_schedule_task = AddScheduleTask(source, destination, date)
        try:
            return self._add_schedule_task.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while adding new flight schedule')
            logging.error('UpdateDate Activity: add_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())
    
    def update_booking(self, booking_id, date, flight_id):
        self._update_booking_task = UpdateBookingTask(booking_id, date, flight_id)
        try:
            return self._update_booking_task.perform_activity()
        except:
            self.set_error_msg(
                'Internal error while updating booking.')
            logging.error('UpdateDate Activity: add_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def do(self):
        booking_table = BookingTableMapper().map(self.check_activity(self._booking_id))
        flightid = booking_table.get_flight_id()
        if booking_table.get_travel_date() == self._date:
            self.set_error_msg(
                'Reschedule date cannot be same as previous date.')
            logging.error('UpdateDate Activity: add_schedule {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())
        try:
            count = self.passenger_count_activity(flightid)
            if int(count) == 1:
                self.remove_schedule_activity(flightid)
        except TypeError as e:
            logging.info(e)
        if self.check_schedule(booking_table.get_src_location(), booking_table.get_dest_location(), self._date) == False:
            flightid = self.add_schedule(booking_table.get_src_location(), booking_table.get_dest_location(), self._date)
        return self.update_booking(booking_table.get_booking_id(), self._date, flightid) + 'new Flight id: {}.'.format(flightid)
        