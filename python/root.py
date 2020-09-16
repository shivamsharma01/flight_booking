import mysql.connector
from datetime import datetime
from flask import Flask, request, jsonify, json

api = Flask(__name__)

mydb=None
mycursor=None

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
  found = False
  for x in mycursor:
    if x[0] == 'booking_table':
      found = True
  if found == False:
    mycursor.execute("CREATE TABLE BOOKING_TABLE (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), src_location VARCHAR(100), dest_location VARCHAR(100), class CHAR(1), travel_date DATETIME)")
  

connectdb()

@api.route('/flightbooking/', methods=["POST"])
def root():    

  def booking(data):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = 'insert into BOOKING_TABLE(name, src_location, dest_location, class, travel_date) VALUES (%s, %s, %s, %s, %s)'
    val = (data['name']+formatted_date, data['src_location'], data['dest_location'], data['class'], data['travel_date'])
    mycursor.execute(sql, val)
    mydb.commit()
    return "{}{}".format("FLY-", mycursor.lastrowid)

  if request.json['type'] == "booking":
    return booking(request.json['data'])
  else:
    return "Failed"
#jsonify(request.json)


if __name__ == '__main__':
  api.run()

