import logging
from common.util.task import Task
from common.util.transaction import Transaction

class AddNewCardTask(Task):
    def __init__(self, balance):
        if balance is None or balance == '':
            self._balance = 10000
        else:
            self._balance = balance

    def perform_activity(self):
        try:
            logging.info('AddNewCard Task: Adding a new Card with balance {}'.format(self._balance))
            transaction = Transaction()
            transaction.execute(
                "INSERT INTO CREDIT_CARD_TABLE(balance) VALUES ({})".format(self._balance))
            logging.info('AddNewCard Task: logged response: row count {}'.format(
                transaction.get_cursor().rowcount))
            return "ISSUED NEW CREDIT CARD NO: {}".format(transaction.execute('SELECT LAST_INSERT_ID()')[0])
        finally:
            transaction.close()
