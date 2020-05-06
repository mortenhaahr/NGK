#!/usr/bin/env python3

from flask import Flask, request, jsonify, redirect, session, json, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from pymongo import MongoClient, DESCENDING
import re # regular expressions used in specific date endpoint
from functools import wraps

# Our files:
from WeatherData import WeatherData, Place
from User import User
from functions import convertObjectId, isDate, deleteOldTokens

# DB config:
with open("config/db_config.json") as json_file:
    dbData = json.load(json_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
mongoClient = MongoClient(dbData['MONGO_DB_CONNECTION_STRING']) # load the client based on config file
mongoDb = mongoClient["NGKWeatherDB"]
weatherCol = mongoDb["WeatherData"] # mongoCollection. 
userCol = mongoDb["Users"]
JWTCol = mongoDb["JWT"]

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({'message' : 'Token is missing!'}), 401

		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = userCol.find({'public_id': data['public_id']}).next()

			JWTObj = JWTCol.find({'token': token}).next()
			if(not JWTObj.get('active')):
				return jsonify({'message' : 'Using inactive token!'}), 401

			current_user = User(name=current_user.get('name'), password=current_user.get('password'), admin=current_user.get('admin'), public_id = current_user.get('public_id'))
		except:
			return jsonify({'message' : 'Token is invalid!'}), 401

		return f(current_user, *args, **kwargs)

	return decorated

@app.route('/user/', methods=['GET'])
@token_required
def get_all_users(current_user):

	if not current_user.admin:
		return jsonify({'message' : 'Not allowed to do that function!'})

	cursor = userCol.find() # make cursor with no sorting
	listOfUserData = list(cursor) # return all the objects as a list and set the cursor to last index
        
	listOfUserData = convertObjectId(listOfUserData) # See function

	return jsonify(listOfUserData),200

@app.route('/user/', methods=['POST'])
def create_user():

	data = request.get_json()

	hashed_password = generate_password_hash(data['password']) # Automatic salt
	new_user = User(name=data['name'], password=hashed_password, admin=False)
	userDict = new_user.convertToDict()
	userCol.insert_one(userDict)

	return jsonify({"message" : "New user created!"}), 200

@app.route('/login/', methods=['POST'])
def login():
	auth = request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	user = userCol.find({"name": auth.username})
	
	if(not user.count()):
		return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	userDict = user.next()
	
	if not userDict:
		return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	if check_password_hash(userDict.get('password'), auth.password):
		tokenDict = {'public_id' : userDict.get('public_id'), 'iat' : datetime.utcnow(), 'exp' : datetime.utcnow() + timedelta(minutes=30)}
		token = jwt.encode(tokenDict, app.config['SECRET_KEY'])
		
		tokenDict['active'] = True
		tokenDict['token'] = token.decode('UTF-8')

		JWTCol.insert_one(tokenDict)

		return jsonify({'token' : token.decode('UTF-8')}), 200
	
	return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/logout/', methods=['POST'])
@token_required
def logout(current_user):

	idQuery = {'public_id': current_user.public_id}
	inactiveQuery = {"$set": {"active" : False}}
	JWTCol.update_many(idQuery, inactiveQuery) # Set all JWT with corresponding public_id to inactive.

	return jsonify({'message' : 'Logged out!'}), 200

@app.route('/flush_tokens/', methods=['POST'])
@token_required
def flush_tokens(current_user):
	if not current_user.admin:
		return jsonify({'message' : 'Not allowed to do that function!'})

	global JWTCol # Must be specified, since we reassign it below
	JWTCol.drop()

	return jsonify({'message' : 'Flushed JWT tokens!'}), 200
	
@app.route('/weather/', methods=['POST'])
@token_required
def post_weather(current_user):
	data = request.get_json()

	"""{
		"place": {
			"name": "Aarhus",
			"lat": 58.986462,
			"lon": 6.190466
		},
		"temp": 13.231,
		"humidity": 54,
		"press": 1030
	}"""

	new_place = Place(name=data['place']['name'], lat=data['place']['lat'], lon=data['place']['lon'])
	new_weather = WeatherData(place=new_place, temperature=data['temp'], humidity=data['humidity'], pressure=data['press'])
	weatherDict = new_weather.convertToDict()
	weatherCol.insert_one(weatherDict)

	return jsonify({"message" : "Posted new weatherdata!"}), 200

if __name__ == '__main__':
	deleteOldTokens(JWTCol)
	app.run(debug=True)