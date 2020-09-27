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
        'booking_table': "CREATE TABLE BOOKING_TABLE (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), src_location VARCHAR(100), dest_location VARCHAR(100), class CHAR(1), booking_status VARCHAR(100), payment_method VARCHAR(100), travel_date DATE)",
        'schedule_table': "CREATE TABLE SCHEDULE_TABLE (id INT AUTO_INCREMENT PRIMARY KEY, capacity INT UNSIGNED, src_location VARCHAR(100), dest_location VARCHAR(100), travel_date DATE)",
    }

    tables = []
    for x in mycursor:
        tables.append(x[0])
    for (t_name, comm) in dictionary.items():
        if t_name not in tables:
            mycursor.execute(comm)


@api.route('/flightbooking/', methods=["POST"])
def root():
    def is_booked(id):
      print(id)
      sql = "SELECT * FROM BOOKING_TABLE WHERE id="+str(id)
      mycursor.execute(sql)
      record = mycursor.fetchone()
      if mycursor.rowcount == 0:
        return False, record
      else:
        return True, record

    def is_Scheduled(src, dest, date):
        sql = "SELECT * FROM SCHEDULE_TABLE WHERE src_location=%s AND dest_location=%s AND travel_date=%s"
        mycursor.execute(sql, (src, dest, date))
        record = mycursor.fetchone()
        if mycursor.rowcount == 0:
            return False, 0
        else:
            return True, record[1]

    def Schedule_flight(src, dest, date, request_type):
        status, capacity = is_Scheduled(src, dest, date)
        if status == False:
            sql = 'insert into SCHEDULE_TABLE(src_location, dest_location, capacity, travel_date) VALUES (%s, %s, %s, %s)'
            mycursor.execute(sql, (src, dest, 49, date))
        else:
            sql = "UPDATE SCHEDULE_TABLE SET capacity =%s WHERE src_location=%s AND dest_location=%s AND travel_date=%s"
            if request_type == 'booking':
              capacity = capacity - 1
            else:
                capacity = capacity + 1
            mycursor.execute(sql, (capacity, src, dest, date))
        mydb.commit()
        if status == False:
            print("{}{}".format("Scheduled-", mycursor.lastrowid))
        else:
            print("Updated Capacity to {}".format(capacity))

    def booking(data):
        date = dateutil.parser.parse(data['travel_date']).date()
        if date < datetime.now().date():
            return "travel date Cannot be older than current date"
        Schedule_flight(data['src_location'], data['dest_location'], date, 'booking')
        # print(status)
        sql = 'insert into BOOKING_TABLE(name, src_location, dest_location, class, booking_status, payment_method, travel_date) VALUES (%s, %s, %s, %s, "PENDING", "PENDING", %s)'
        val = (data['name'], data['src_location'], data['dest_location'],
               data['class'], dateutil.parser.parse(data['travel_date']).date())
        mycursor.execute(sql, val)
        mydb.commit()
        return "{}{}".format("FLY-", mycursor.lastrowid)

    def cancel(data):
      id = data['id']
      status, record = is_booked(id)
      if status == False:
        return "No reservation Available. Please check the booking id"
      else:
        sql = "DELETE FROM BOOKING_TABLE WHERE id="+str(id)
        Schedule_flight(record[2], record[3], record[7], 'cancel')
        mycursor.execute(sql)
        mydb.commit()
        if mycursor.rowcount == 0:
          return "Flight could not be canceled"
        else:
          return "Flight with bookingid {} canceled".format(id)

    if request.json['type'] == "booking":
        return booking(request.json['data'])
    elif request.json['type'] == "cancel":
        return cancel(request.json['data'])
    else:
        return "Failed"


if __name__ == '__main__':
    connectdb()
    api.run()
