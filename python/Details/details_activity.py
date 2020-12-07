import logging
from common.util.activity import Activity
from common.util.exception import NoBookingError
from Details.details_task import DetailsTask


class DetailsActivity(Activity):
    def __init__(self, balance):
        self._balance = balance
        self._details = None

    def details_activity(self, balance):
        self._details = DetailsTask(balance)
        try:
            return self._details.perform_activity()
        except NoBookingError as nbe:
            self.set_error_msg(nbe.message)
            logging.error('Details Activity: details_activity {}'.format(
                self.get_error_msg()))
            raise nbe
        except:
            self.set_error_msg('Internal error while fetching the details')
            logging.error('NewCard Activity: details_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def do(self):
        return self.details_activity(self._balance)
