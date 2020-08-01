import time
import json
from datetime import datetime
import os
from flask import Flask,request,jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
# Database
#Server: sql12.freemysqlhosting.net
#Name: sql12357988
#Username: sql12357988
#Password: jbkqb3Bf9n
#Port number: 3306


#mysql://sql12357988:jbkqb3Bf9n@sql12.freemysqlhosting.net:3306/sql12357988
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql12357988:jbkqb3Bf9n@sql12.freemysqlhosting.net:3306/sql12357988'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    start_time = db.Column(db.DateTime,default=datetime.now)
    thumbnail = db.Column(db.String(50),default='')
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, name, start_time, thumbnail, active, date_created):
        self.name = name
        self.start_time = start_time
        self.thumbnail = thumbnail
        self.active = active
        self.date_created = date_created

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'start_time', 'thumbnail', 'active', 'date_created')


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


#localhost:5000/addUser
"""
{
    "name":"Name",
    "start_time":"09/19/18 13:55:26"",
    "thumbnail":"",
    "active":"1",
    "date_created":""
}
"""

#localhost:5000/addUser
@app.route('/addUser', methods=['POST'])
def add_user():
    name = request.json['name']
    start_time = datetime.now() if request.json['start_time']=="" else datetime.strptime(request.json['start_time'], '%m/%d/%y %H:%M:%S')
    thumbnail = request.json['thumbnail']
    active = False if request.json['active']=="0" else True
    date_created = datetime.now() if request.json['date_created']=="" else datetime.strptime(request.json['date_created'], '%m/%d/%y %H:%M:%S')

    new_user = User(name, start_time, thumbnail, active, date_created)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


#localhost:5000/allUsers
@app.route('/allUsers', methods=['GET'])
def get_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)


#localhost:5000/activeCount
@app.route('/activeCount', methods=['GET'])
def get_activeCount():
    count = User.query.filter(User.active == True).count()
    return jsonify(count)


#localhost:5000/activeList
@app.route('/activeList', methods=['GET'])
def get_activeList():
    acive_users = User.query.filter(User.active == True)
    result = users_schema.dump(acive_users)
    return jsonify(result)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}
