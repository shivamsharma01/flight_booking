class Booking:
    def __init__(self):
        self._name = None
        self._src_location = None
        self._dest_location = None
        self._flight_class = None
        self._travel_date = None
        self._flight_id = None
        self._booking_id = None
        self._booking_status = None
        self._payment_method = None
        self._card_no = None
        self._add_on = None

    def get_name(self): 
        return self._name
      
    def set_name(self, name): 
        self._name = name

    def get_src_location(self): 
        return self._src_location 
      
    def set_src_location(self, src_location): 
        self._src_location = src_location
    
    def get_dest_location(self): 
        return self._dest_location 
      
    def set_dest_location(self, dest_location): 
        self._dest_location = dest_location
    
    def get_flight_class(self): 
        return self._flight_class
      
    def set_flight_class(self, flight_class): 
        self._flight_class = flight_class

    def get_travel_date(self): 
        return self._travel_date 

    def set_travel_date(self, travel_date): 
        self._travel_date = travel_date

    def get_flight_id(self):
        return self._flight_id
    
    def set_flight_id(self, flight_id):
        self._flight_id = flight_id

    def get_booking_id(self):
        return self._booking_id

    def set_booking_id(self, booking_id):
        self._booking_id = booking_id

    def get_booking_status(self):
        return self._booking_status

    def set_booking_status(self, booking_status):
        self._booking_status = booking_status
    
    def get_payment_method(self):
        return self._payment_method

    def set_payment_method(self, payment_method):
        self._payment_method = payment_method

    def get_card_no(self):
        return self._card_no

    def set_card_no(self, card_no):
        self._card_no = card_no

    def get_add_on(self):
        return self._add_on

    def set_add_on(self, add_on):
        self._add_on = add_on
