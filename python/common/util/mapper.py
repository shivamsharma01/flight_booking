from common.util.dateutility import DateUtility
from common.util.booking import Booking
from common.util.card import CreditCard
import sys
sys.path.append(".")


class Mapper:
    def map(self, request):
        pass


class BookMapper(Mapper):
    def map(self, request):
        booking = Booking()
        booking.set_name(request['name'])
        booking.set_src_location(request['src_location'])
        booking.set_dest_location(request['dest_location'])
        booking.set_flight_class(request['flight_class'])
        booking.set_travel_date(
            DateUtility.date_converter(request['travel_date']))
        return booking


class CancelMapper(Mapper):
    def map(self, request):
        booking = Booking()
        booking.set_booking_id(request['booking_id'])
        return booking


class BookingTableMapper(Mapper):
    def map(self, request):
        booking = Booking()
        booking.set_booking_id(request[0])
        booking.set_name(request[1])
        booking.set_src_location(request[2])
        booking.set_dest_location(request[3])
        booking.set_flight_class(request[4])
        booking.set_booking_status(request[5])
        booking.set_payment_method(request[6])
        booking.set_card_no(request[7])
        booking.set_travel_date(request[8])
        booking.set_flight_id(request[9])
        booking.set_add_on(request[10])
        return booking


class CreditCardMapper(Mapper):
    def map(self, request):
        card = CreditCard()
        card.set_card_number(request[0])
        card.set_balance(request[1])
        return card


class PaymentMapper(Mapper):
    def map(self, request):
        booking = Booking()
        booking.set_card_no(request['card_number'])
        booking.set_booking_id(request['booking_id'])
        return booking


class UpdateDateMapper(Mapper):
    def map(self, request):
        booking = Booking()
        booking.set_travel_date(DateUtility.date_converter(request['travel_date']))
        booking.set_booking_id(request['booking_id'])
        return booking


class AddOnMapper(Mapper):
    def map(self, request):
        booking = Booking()
        booking.set_booking_id(request['booking_id'])
        booking.set_card_no(request['card_number'])
        return booking


class NewCardMapper(Mapper):
    def map(self, request):
        return request.args.get("balance")

class DeatilsMapper(Mapper):
    def map(self, request):
        return request.json['booking_id']