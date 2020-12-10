from flask_sqlalchemy import SQLAlchemy
import datetime
from hotel import app
db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, index=True)
    dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, firstname, lastname, username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email


class Posts(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    puid = db.Column(db.Integer, db.ForeignKey('user.uid'))

    def __init__(self, title, description, puid):
        self.title = title
        self.description = description
        self.puid = puid

class Room_type(db.Model):
    tid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    type_name = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    def __init__(self, type_name, description):
        self.type_name = type_name
        self.description = description

class Rooms(db.Model):
    # rid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    room_number = db.Column(db.Integer,primary_key=True)
    room_type = db.Column(db.Integer,db.ForeignKey('room_type.tid'))
    cost = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(100))

    def __init__(self, room_type, cost, capacity,status):
        self.room_type = room_type
        self.cost = cost
        self.capacity = capacity
        self.status = status

class Reservations(db.Model):
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ruid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    num_guests = db.Column(db.Integer)

    def __init__(self, ruid, checkin_date, checkout_date,num_guests):
        self.ruid = ruid
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.num_guests = num_guests

class Booked(db.Model):
    bid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brid = db.Column(db.Integer, db.ForeignKey('reservations.rid'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_number'))

    def __init__(self, brid, room_id):
        self.brid = brid
        self.room_id = room_id
db.create_all()
