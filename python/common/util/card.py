class CreditCard:
    def __init__(self):
        self._card_number = None
        self._balance = None

    def get_card_number(self): 
        return self._card_number
      
    def set_card_number(self, card_number): 
        self._card_number = card_number

    def get_balance(self): 
        return self._balance
      
    def set_balance(self, balance): 
        self._balance = balance