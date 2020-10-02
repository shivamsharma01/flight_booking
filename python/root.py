import mysql.connector
from datetime import datetime
import dateutil.parser
from flask import Flask, request, jsonify, json

api = Flask(__name__)

mydb = None
mycursor = None


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

    dictionary = {
        'booking_table': "CREATE TABLE BOOKING_TABLE (booking_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), src_location VARCHAR(100), dest_location VARCHAR(100), class CHAR(1), booking_status VARCHAR(100), payment_method VARCHAR(100), card_number INT UNSIGNED, travel_date DATE, flight_id INT UNSIGNED)",
        'schedule_table': "CREATE TABLE SCHEDULE_TABLE (flight_id INT AUTO_INCREMENT PRIMARY KEY, src_location VARCHAR(100), dest_location VARCHAR(100), travel_date DATE)",
        'credit_card_table': "CREATE TABLE CREDIT_CARD_TABLE (card_number INT AUTO_INCREMENT PRIMARY KEY, balance INT)",
    }

    tables = []
    for x in mycursor:
        tables.append(x[0])
    for (t_name, comm) in dictionary.items():
        if t_name not in tables:
            mycursor.execute(comm)


@api.route('/flightbooking/', methods=["POST"])
def root():
    price = {'B': 10000, 'E': 5000, 'F': 20000}

    def date_converter(date):
        return dateutil.parser.parse(date).date()

    def is_past_date(date):
        return date < datetime.now().date()

    def get_no_of_passengers(flight_id):
        sql = "SELECT count(*) FROM BOOKING_TABLE WHERE flight_id=" + \
            str(flight_id)
        mycursor.execute(sql)
        record = mycursor.fetchone()
        return record[0]

    def delete_flight_schedule(flight_id):
        sql = "DELETE FROM SCHEDULE_TABLE WHERE flight_id="+str(flight_id)
        mycursor.execute(sql)
        mydb.commit()

    def is_booked(id):
        sql = "SELECT * FROM BOOKING_TABLE WHERE booking_id="+str(id)
        mycursor.execute(sql)
        record = mycursor.fetchone()
        if mycursor.rowcount == 0:
            return False, 0
        else:
            return True, record

    def confirm_booking(id, card_number):
        sql = "UPDATE BOOKING_TABLE SET booking_status=%s, payment_method=%s, card_number=%s WHERE booking_id=%s" 
        mycursor.execute(sql, ("CONFIRMED", "CREDIT_CARD", card_number, id))
        mydb.commit()
        return mycursor.rowcount

    def is_Scheduled(src, dest, date):
        sql = "SELECT * FROM SCHEDULE_TABLE WHERE src_location=%s AND dest_location=%s AND travel_date=%s"
        mycursor.execute(sql, (src, dest, date))
        record = mycursor.fetchone()
        if mycursor.rowcount == 0:
            return False, 0
        else:
            return True, record

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

    def make_transaction(booking_id, card_number, amount, t_type):
        print("{} {} {} {}".format(booking_id, card_number, amount, t_type))
        sql = "SELECT * FROM CREDIT_CARD_TABLE WHERE card_number="+str(card_number)
        mycursor.execute(sql)
        record = mycursor.fetchone()
        if mycursor.rowcount == 0:
            return False, "This credit card is invalid!!!"
        else:
            sql = "UPDATE CREDIT_CARD_TABLE SET balance = %s WHERE card_number=%s"
            if t_type == 'credit':
                amount = int(record[1]) + int(amount)
                mycursor.execute(sql, (amount, card_number))
                mydb.commit()
                return True, 'Rs.{} refunded.'.format(amount)
            else:
                amount = int(record[1]) - int(amount)
                mycursor.execute(sql, (amount, card_number))
                mydb.commit()
                confirm_booking(booking_id, card_number)
                return True, "Booking Confirmed"
    '''

    request payload 
    {
        "type": "booking",
        "data": {
            "name": "Fourth",
            "src_location": "Delhi",
            "dest_location": "Mumbai",
            "class": "B",
            "travel_date": "2020-09-27 15:37:53.706358"
        }
    }

    response error
        travel date Cannot be older than current date
        
    response success
    {
        "FLY-XXXX" //XXXX is the booking id
    }
    '''
    def booking(data):
        date = date_converter(data['travel_date'])
        if is_past_date(date) == True:
            return "travel date Cannot be older than current date"
        flight_id = Schedule_flight(
            data['src_location'], data['dest_location'], date, 'booking')
        sql = 'insert into BOOKING_TABLE(name, src_location, dest_location, class, booking_status, payment_method, travel_date, flight_id) VALUES (%s, %s, %s, %s, "PENDING", "PENDING", %s, %s)'
        mycursor.execute(sql, (data['name'], data['src_location'], data['dest_location'],
                               data['class'], date, flight_id))
        mydb.commit()
        return "{}{}".format("FLY-", mycursor.lastrowid)

    '''

    request payload 
    {
        "type": "cancel",
        "data": {
            "id": "3"
        }
    }

    response error
        "No reservation Available. Please check the booking id"
        "Flight could not be canceled"
        
    response success
    {
        "Flight with bookingid X canceled"
    }
    '''

    def cancel(data):
        id = data['booking_id']
        status, record = is_booked(id)
        if status == False:
            return "No reservation Available. Please check the booking id"
        
        msg = ''
        if (record[5] == 'CONFIRMED'):
            card_number = int(record[7])
            print(card_number)
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
            return "Flight could not be canceled"
        else:
            return "Flight with bookingid {} canceled. {}".format(id, msg)

    def confirm_payment(data):
        id = data['booking_id']
        card_number = data['card_number']
        status, record = is_booked(id)
        if status == False:
            return "No reservation Available. Please check the booking id"
        elif (record[5] == 'CONFIRMED'):
            return "This Flight is already Confirmed!!!"
        else:
            flight_class = record[4]
            amount = price[flight_class]
            status, message = make_transaction(id, card_number, amount, 'debit')
            return message

    if request.json['type'] == "booking":
        return booking(request.json['data'])
    elif request.json['type'] == "cancel":
        return cancel(request.json['data'])
    elif request.json['type'] == "payment":
        return confirm_payment(request.json['data'])
    # elif request.json['type'] == "update-date":
    #     return change_date(request.json['data'])
    # elif request.json['type'] == "add-on":
    #     return cancel(request.json['data'])
    # elif request.json['type'] == "add-on":
    #     return cancel(request.json['data'])
    else:
        return "Failed"


if __name__ == '__main__':
    connectdb()
    api.run()
