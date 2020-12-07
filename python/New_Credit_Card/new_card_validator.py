import sys
sys.path.append(".")
import logging
from common.util.field_validator import BalanceValidator
from common.util.service_validator import ServiceValidator

class NewCardValidator(ServiceValidator):
    def __init__(self, balance):
        self._error_msg = None
        self._balance = balance

    def validate(self):
        balanceValidator = BalanceValidator(self._balance)
        if balanceValidator.validate() == False:
            logging.warning('NewCardValidator: Balance Validator: {}'.format(self._balance))
            self._error_msg = balanceValidator.get_error_msg()
            return False
        return True
    
    def get_error_msg(self):
        return self._error_msg
