import json


class Object:

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Response:

    @staticmethod
    def create_booking_response(booking_id):
        obj = Object()
        obj.error = False
        obj.booking_id = booking_id
        return obj.toJSON()

    @staticmethod
    def create_cancel_response(message):
        obj = Object()
        obj.error = False
        obj.success_msg = message
        return obj.toJSON()

    @staticmethod
    def create_confirm_payment_response(message):
        obj = Object()
        obj.error = False
        obj.success_msg = message
        return obj.toJSON()

    @staticmethod
    def create_update_date_obj(message):
        obj = Object()
        obj.error = False
        obj.success_msg = message
        return obj.toJSON()

    @staticmethod
    def create_new_card_obj(message):
        obj = Object()
        obj.error = False
        obj.success_msg = message
        return obj.toJSON()

    @staticmethod
    def create_add_luggage_obj(message):
        obj = Object()
        obj.error = False
        obj.success_msg = message
        return obj.toJSON()

    @staticmethod
    def create_details_response(booking):
        obj = Object()
        obj.error = False
        obj.booking_id = booking.get_booking_id()
        obj.name = booking.get_name()
        obj.src = booking.get_src_location()
        obj.dest = booking.get_dest_location()
        obj.flight_class = booking.get_flight_class()
        obj.booking_status = booking.get_booking_status()
        obj.payment_method = booking.get_payment_method()
        obj.card_no = booking.get_card_no()
        obj.travel_date = str(booking.get_travel_date())
        obj.flight_id = booking.get_flight_id()
        obj.add_on = booking.get_add_on()
        return obj.toJSON()

    @staticmethod
    def create_error_obj(error, msg):
        obj = Object()
        obj.error = error
        obj.message = msg
        return obj.toJSON()