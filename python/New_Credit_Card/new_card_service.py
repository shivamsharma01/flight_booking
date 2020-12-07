from New_Credit_Card.new_card_validator import NewCardValidator
from common.util.service import Service
from common.util.mapper import NewCardMapper
from New_Credit_Card.new_card_activity import NewCardActivity
import sys
sys.path.append(".")

class NewCardService(Service):
    def __init__(self, card_request):
        balance = NewCardMapper().map(card_request)
        super().__init__(NewCardValidator(balance), NewCardActivity(balance))
