import logging
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
from common.util.response import Response
from common.util.transaction import Transaction
from common.util.exception import NoBookingError
from common.util.mapper import BookingTableMapper
from Booking.booking_service import BookingService
from Cancel.cancel_service import CancelService
from Payment.payment_service import PaymentService
from Update_Date.update_date_service import UpdateDateService
from New_Credit_Card.new_card_service import NewCardService
from Add_On.add_on_service import AddOnService
from Details.details_service import DetailsService

api = Flask(__name__)
CORS(api)


@api.route("/")
def app_test():
    return "App is Working. Time is {}".format(datetime.now())


'''
Function to book a ticket from source to destination
    - validate date- should not be a date from past
    - schedule a flight from given source to destination on a given day if user is the first passenger 
    - add entry in booking take
    - returns booking id
'''

@api.route('/flightbooking/book', methods=["POST"])
def booking():
    booking_service = BookingService(request.json)
    booking_validator = booking_service.get_validator()
    if booking_validator.validate() == False:
        return Response.create_error_obj(True, booking_validator.get_error_msg())
    booking_activity = booking_service.get_activity()
    try:
        return Response.create_booking_response(booking_activity.do())
    except:
        return Response.create_error_obj(True, booking_activity.get_error_msg())


'''
    Function to cancel a ticket using booking id
        - validate booking - entry should be present
        - if ticket is not confirmed - cancel the flight
        - if ticket is confirmed - deduct 50% amount and refund remaining to the attached credit card number
        - no refund for luggage
        - returns a message
    '''
@api.route('/flightbooking/cancel', methods=["POST"])
def cancel():
    cancel_service = CancelService(request.json)
    cancel_validator = cancel_service.get_validator()
    if cancel_validator.validate() == False:
        return Response.create_error_obj(True, cancel_validator.get_error_msg())
    cancel_activity = cancel_service.get_activity()
    try:
        return Response.create_cancel_response(cancel_activity.do())
    except:
        return Response.create_error_obj(True, cancel_activity.get_error_msg())


'''
    Function to confirm a ticket using booking id and credit card number
        - validate booking - entry should be present
        - validate status - status should be pending
        - validate credit card - should be a valid credit card
        - returns a message
    '''
@api.route('/flightbooking/confirm_payment', methods=["POST"])
def confirm_payment():
    payment_service = PaymentService(request.json)
    payment_validator = payment_service.get_validator()
    if payment_validator.validate() == False:
        return Response.create_error_obj(True, payment_validator.get_error_msg())
    payment_activity = payment_service.get_activity()
    try:
        return Response.create_confirm_payment_response(payment_activity.do())
    except:
        return Response.create_error_obj(True, payment_activity.get_error_msg())


'''
    Function to change the date using booking id
        - validate date - should not be a date from past
        - validate date - should be a different date
        - validate booking - entry should be present
        - validate status - status should be confirmed
        - validate date - should be a different date
        - returns a message
    '''
@api.route('/flightbooking/update_date', methods=["POST"])
def update_date():
    update_date_service = UpdateDateService(request.json)
    update_date_validator = update_date_service.get_validator()
    if update_date_validator.validate() == False:
        return Response.create_error_obj(True, update_date_validator.get_error_msg())
    update_date_activity = update_date_service.get_activity()
    try:
        return Response.create_update_date_obj(update_date_activity.do())
    except:
        return Response.create_error_obj(True, update_date_activity.get_error_msg())


@api.route('/flightbooking/create_user', methods=["GET"])
def create_credit_card_user():
    new_card_service = NewCardService(request)
    new_card_validator = new_card_service.get_validator()
    if new_card_validator.validate() == False:
        return Response.create_error_obj(True, new_card_validator.get_error_msg())
    new_card_activity = new_card_service.get_activity()
    try:
        return Response.create_new_card_obj(new_card_activity.do())
    except:
        return Response.create_error_obj(True, new_card_activity.get_error_msg())


'''
    Function to add luggage to the booking
        - validate credit card - should be a valid credit card
        - validate booking - entry should be present
        - validate booking status - status should be confirmed
        - validate add on status - should not be already confirmed 
        - returns a message
    '''
@api.route('/flightbooking/add_on', methods=["POST"])
def add_luggage():
    add_on_service = AddOnService(request.json)
    add_on_validator = add_on_service.get_validator()
    if add_on_validator.validate() == False:
        return Response.create_error_obj(True, add_on_validator.get_error_msg())
    add_on_activity = add_on_service.get_activity()
    try:
        return Response.create_add_luggage_obj(add_on_activity.do())
    except:
        return Response.create_error_obj(True, add_on_activity.get_error_msg())


'''
Function to get the details of the booking
    - validate booking - entry should be present
    - returns the complete entry in db
'''
@api.route('/flightbooking/details', methods=["POST"])
def details():
    details_service = DetailsService(request)
    details_validator = details_service.get_validator()
    if details_validator.validate() == False:
        return Response.create_error_obj(True, details_validator.get_error_msg())
    details_activity = details_service.get_activity()
    try:
        return Response.create_details_response(BookingTableMapper().map(details_activity.do()))
    except NoBookingError as e:
        return Response.create_error_obj(True, e.message)
    except:
        return Response.create_error_obj(True, details_activity.get_error_msg())


dictionary = {
    'booking_table': "CREATE TABLE BOOKING_TABLE (booking_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), src_location VARCHAR(100), dest_location VARCHAR(100), class CHAR(1), booking_status VARCHAR(100), payment_method VARCHAR(100), card_number INT UNSIGNED, travel_date DATE, flight_id INT UNSIGNED, add_on VARCHAR(100))",
    'schedule_table': "CREATE TABLE SCHEDULE_TABLE (flight_id INT AUTO_INCREMENT PRIMARY KEY, src_location VARCHAR(100), dest_location VARCHAR(100), travel_date DATE)",
    'credit_card_table': "CREATE TABLE CREDIT_CARD_TABLE (card_number INT AUTO_INCREMENT PRIMARY KEY, balance INT)",
}

'''
    call the below functions on running this py file automatically.
'''
if __name__ == '__main__':
    logging.basicConfig(filename='logs.txt', filemode='w',
                        format='%(levelname)s:%(message)s', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    transaction = Transaction()
    cursor = transaction.get_cursor()
    cursor.execute("SHOW TABLES")
    tables = []
    for x in cursor:
        tables.append(x[0])
    for (t_name, comm) in dictionary.items():
        if t_name not in tables:
            cursor.execute(comm)
            if (t_name == 'credit_card_table'):
                cursor.execute(
                    "INSERT INTO CREDIT_CARD_TABLE(balance) VALUES (10000)")
    transaction.close()
    api.run()
