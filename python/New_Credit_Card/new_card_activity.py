import logging
from common.util.activity import Activity
from New_Credit_Card.new_card_task import AddNewCardTask

class NewCardActivity(Activity):
    def __init__(self, balance):
        self._balance = balance
        self._add_card_task = None

    def add_card_activity(self, balance):
        self._add_card_task = AddNewCardTask(balance)
        try:
            return self._add_card_task.perform_activity()
        except:
            self.set_error_msg('Internal error while creating the card')
            logging.error('NewCard Activity: add_card_activity {}'.format(
                self.get_error_msg()))
            raise TypeError(self.get_error_msg())

    def do(self):
        return self.add_card_activity(self._balance)
