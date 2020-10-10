import mysql.connector
from datetime import datetime
import dateutil.parser
from flask import Flask, request
from flask_cors import CORS

api = Flask(__name__)
CORS(api)

mydb = None
mycursor = None

# this function will be called when application is loaded. This db instance will be used across to access the db
def connectdb():
    print("starting db")
    global mydb
    global mycursor
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxxaaaa",
        database="flight"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")

    # Create the below tables if not already present in the db
    dictionary = {
        'booking_table': "CREATE TABLE BOOKING_TABLE (booking_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), src_location VARCHAR(100), dest_location VARCHAR(100), class CHAR(1), booking_status VARCHAR(100), payment_method VARCHAR(100), card_number INT UNSIGNED, travel_date DATE, flight_id INT UNSIGNED, add_on VARCHAR(100))",
        'schedule_table': "CREATE TABLE SCHEDULE_TABLE (flight_id INT AUTO_INCREMENT PRIMARY KEY, src_location VARCHAR(100), dest_location VARCHAR(100), travel_date DATE)",
        'credit_card_table': "CREATE TABLE CREDIT_CARD_TABLE (card_number INT AUTO_INCREMENT PRIMARY KEY, balance INT)",
    }

    tables = []
    for x in mycursor:
        tables.append(x[0])
    for (t_name, comm) in dictionary.items():
        if t_name not in tables:
            mycursor.execute(comm)
            if (t_name == 'credit_card_table')
            mycursor.execute(
                "INSERT INTO CREDIT_CARD_TABLE(balance) VALUES (10000)")
        mydb.commit()

# the root of the entire application/root node in the cartesian/modular structure


@api.route('/flightbooking/', methods=["POST"])
def root():
    # predefined ticket prices B = business class, E = economy class, F = First class
    price = {'B': 10000, 'E': 5000, 'F': 20000}

    # utility function for date. Returns only date part
    def date_converter(date):
        return dateutil.parser.parse(date).date()

    # validation function for date
    def is_past_date(date):
        print(datetime.date)
        print(datetime.now().date())
        print(date)
        return date < datetime.now().date()

    # no of passengers in the flight (specific date and from a particular source to Destination)
    def get_no_of_passengers(flight_id):
        sql = "SELECT count(*) FROM BOOKING_TABLE WHERE flight_id=" + \
            str(flight_id)
        mycursor.execute(sql)
        record = mycursor.fetchone()
        return record[0]

    # When the last booking in a particular flight is cancelled / no of passengers = 0
    def delete_flight_schedule(flight_id):
        sql = "DELETE FROM SCHEDULE_TABLE WHERE flight_id="+str(flight_id)
        mycursor.execute(sql)
        mydb.commit()

    # Used to make a valid entry in db in credit card table
    def create_credit_card_user():
        sql = "INSERT INTO CREDIT_CARD_TABLE(balance) VALUES (10000)"
        mycursor.execute(sql)
        mydb.commit()
        return "ISSUED NEW CREDIT CARD NO: {}".format(mycursor.rowcount)

    # check if the booking_id exists in db
    def is_booked(id):
        sql = "SELECT * FROM BOOKING_TABLE WHERE booking_id="+str(id)
        mycursor.execute(sql)
        record = mycursor.fetchone()
        if mycursor.rowcount == 0:
            return False, 0
        else:
            return True, record

    # confirms the booking after valid credit card details are entered
    def confirm_booking(id, card_number):
        sql = "UPDATE BOOKING_TABLE SET booking_status=%s, payment_method=%s, card_number=%s WHERE booking_id=%s"
        mycursor.execute(sql, ("CONFIRMED", "CREDIT_CARD", card_number, id))
        mydb.commit()
        return mycursor.rowcount

    # maps a booking with a flight
    def update_flight(booking_id, date, flight_id):
        sql = "UPDATE BOOKING_TABLE SET flight_id=%s, travel_date=%s WHERE booking_id=%s"
        mycursor.execute(sql, (flight_id, date, booking_id))
        mydb.commit()
        return mycursor.rowcount

    # adds luggae entry for the mentioned booking id if credit card details are valid
    def add_luggage(booking_id, card_number):
        status, message = make_transaction(
            booking_id, card_number, 500, 'debit')
        if status == False:
            return message
        sql = "UPDATE BOOKING_TABLE SET add_on=%s WHERE booking_id=%s"
        mycursor.execute(sql, ("YES", booking_id))
        mydb.commit()
        return "Congratulations!!! Luggage Facility is updated."

    # check if there is a flight schedule from given source to destination on a given day
    def is_Scheduled(src, dest, date):
        sql = "SELECT * FROM SCHEDULE_TABLE WHERE src_location=%s AND dest_location=%s AND travel_date=%s"
        mycursor.execute(sql, (src, dest, date))
        record = mycursor.fetchone()
        if mycursor.rowcount == 0:
            return False, 0
        else:
            return True, record

    # schedule a flight from given source to destination on a given day
    def Schedule_flight(src, dest, date, request_type):
        status, record = is_Scheduled(src, dest, date)
        if (request_type == 'booking'):
            if status == False:
                sql = 'insert into SCHEDULE_TABLE(src_location, dest_location, travel_date) VALUES (%s, %s, %s)'
                mycursor.execute(sql, (src, dest, date))
                mydb.commit()
                status, record = is_Scheduled(src, dest, date)
            return record[0]
        return status

    # debit/credit from given credit card
    def make_transaction(booking_id, card_number, amount, t_type):
        sql = "SELECT * FROM CREDIT_CARD_TABLE WHERE card_number=" + \
            str(card_number)
        mycursor.execute(sql)
        record = mycursor.fetchone()
        if mycursor.rowcount == 0:
            return False, "This credit card is invalid!!!"
        else:
            sql = "UPDATE CREDIT_CARD_TABLE SET balance = %s WHERE card_number=%s"
            if t_type == 'credit':
                new_amount = int(record[1]) + int(amount)
                mycursor.execute(sql, (new_amount, card_number))
                mydb.commit()
                return True, 'Rs.{} refunded.'.format(amount)
            else:
                amount = int(record[1]) - int(amount)
                mycursor.execute(sql, (amount, card_number))
                mydb.commit()
                confirm_booking(booking_id, card_number)
                return True, "Booking Confirmed"

    '''
    Function to book a ticket from source to destination
        - validate date- should not be a date from past
        - schedule a flight from given source to destination on a given day if user is the first passenger 
        - add entry in booking take
        - returns booking id
    '''
    def booking(data):
        date = date_converter(data['travel_date'])
        if is_past_date(date) == True:
            return {"error": True, "message": "travel date Cannot be older than current date"}
        flight_id = Schedule_flight(
            data['src_location'], data['dest_location'], date, 'booking')
        sql = 'insert into BOOKING_TABLE(name, src_location, dest_location, class, booking_status, payment_method, travel_date, flight_id, add_on) VALUES (%s, %s, %s, %s, "PENDING", "PENDING", %s, %s, "NO")'
        mycursor.execute(sql, (data['name'], data['src_location'], data['dest_location'],
                               data['class'], date, flight_id))
        mydb.commit()
        return {"error": False, "message": "{}{}".format("FLY-", mycursor.lastrowid)}

    '''
    Function to cancel a ticket using booking id
        - validate booking - entry should be present
        - if ticket is not confirmed - cancel the flight
        - if ticket is confirmed - deduct 50% amount and refund remaining to the attached credit card number
        - no refund for luggage
        - returns a message
    '''
    def cancel(data):
        id = data['booking_id']
        status, record = is_booked(id)
        if status == False:
            return {"error": True, "message": "No reservation Available. Please check the booking id"}
        msg = ''
        if (record[5] == 'CONFIRMED'):
            card_number = int(record[7])
            amount = price[record[4]]*.5
            status, msg = make_transaction(id, card_number, amount, 'credit')
        flight_id = record[9]
        passengers = get_no_of_passengers(flight_id)
        if passengers == 1:
            delete_flight_schedule(flight_id)
        sql = "DELETE FROM BOOKING_TABLE WHERE booking_id="+str(id)
        mycursor.execute(sql)
        mydb.commit()
        if mycursor.rowcount == 0:
            return {"error": True, "message": "Flight could not be canceled"}
        else:
            return {"error": False, "message": "Flight with bookingid {} canceled. {}".format(id, msg)}

    '''
    Function to confirm a ticket using booking id and credit card number
        - validate booking - entry should be present
        - validate status - status should be pending
        - validate credit card - should be a valid credit card
        - returns a message
    '''
    def confirm_payment(data):
        id = data['booking_id']
        card_number = data['card_number']
        status, record = is_booked(id)
        if status == False:
            return {"error": True, "message": "No reservation Available. Please check the booking id"}
        elif (record[5] == 'CONFIRMED'):
            return {"error": True, "message": "This Flight is already Confirmed!!!"}
        else:
            flight_class = record[4]
            amount = price[flight_class]
            status, message = make_transaction(
                id, card_number, amount, 'debit')
            return {"error": False, "message": message}

    '''
    Function to change the date using booking id
        - validate date - should not be a date from past
        - validate date - should be a different date
        - validate booking - entry should be present
        - validate status - status should be confirmed
        - validate date - should be a different date
        - returns a message
    '''
    def update_date(data):
        date = date_converter(data['travel_date'])
        if is_past_date(date) == True:
            return {"error": True, "message": "travel date Cannot be older than current date"}
        id = data['booking_id']
        status, record = is_booked(id)
        if status == False:
            return {"error": True, "message": "No reservation Available. Please check the booking id"}
        else:
            if date == record[8]:
                return {"error": True, "message": "Reschedule date is same as booked date.!!!"}
            flight_id = record[9]
            passengers = get_no_of_passengers(flight_id)
            if passengers == 1:
                delete_flight_schedule(flight_id)
            flight_id = Schedule_flight(record[2], record[3], date, 'booking')
            return {"error": False, "message": "Congratulations!!! your flight has been rescheduled. New flight id is {}".format(update_flight(id, date, flight_id))}

    '''
    Function to add luggage to the booking
        - validate credit card - should be a valid credit card
        - validate booking - entry should be present
        - validate booking status - status should be confirmed
        - validate add on status - should not be already confirmed 
        - returns a message
    '''
    def add_on(data):
        id = data['booking_id']
        card_number = data['card_number']
        status, record = is_booked(id)
        if status == False:
            return {"error": True, "message": "No reservation Available. Please check the booking id"}
        elif (record[5] == 'PENDING'):
            return {"error": True, "message": "Cannot add luggage facility!!! Flight is not confirmed."}
        elif (record[10] == "YES"):
            return {"error": True, "message": "Luggage Facility Already Availed!!!"}
        else:
            return {"error": False, "message": add_luggage(id, card_number)}

    '''
    Function to get the details of the booking
        - validate booking - entry should be present
        - returns the complete entry in db
    '''
    def details(data):
        id = data['booking_id']
        status, record = is_booked(id)
        if status == False:
            return {"error": True, "message": "No reservation Available. Please check the booking id"}
        else:
            return {"error": False, "data": record}

    if request.json['type'] == "booking":
        return booking(request.json['data'])
    elif request.json['type'] == "cancel":
        return cancel(request.json['data'])
    elif request.json['type'] == "payment":
        return confirm_payment(request.json['data'])
    elif request.json['type'] == "update-date":
        return update_date(request.json['data'])
    elif request.json['type'] == "credit-card":
        return create_credit_card_user()
    elif request.json['type'] == "add-on":
        return add_on(request.json['data'])
    elif request.json['type'] == "details":
        return details(request.json['data'])
    else:
        return "Failed"


if __name__ == '__main__':
    connectdb()
    api.run()
