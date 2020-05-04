#!/usr/bin/env python3

from flask import Flask, request, jsonify, redirect, session, json, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
import datetime
from pymongo import MongoClient, DESCENDING
import re # regular expressions used in specific date endpoint
from functools import wraps

# Our files:
from WeatherData import WeatherData
from User import User
from functions import convertObjectId, isDate

# DB config:
with open("config/db_config.json") as json_file:
    dbData = json.load(json_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
mongoClient = MongoClient(dbData['MONGO_DB_CONNECTION_STRING']) # load the client based on config file
mongoDb = mongoClient["NGKWeatherDB"]
weatherCol = mongoDb["WeatherData"] # mongoCollection. 
userCol = mongoDb["Users"]

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
			print(token)

		if not token:
			return jsonify({'message' : 'Token is missing!'}), 401

		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = userCol.find({'public_id': data['public_id']}).next()
			current_user = User(name=current_user.get('name'), password=current_user.get('password'), admin=current_user.get('admin'))
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

	return json.dumps(listOfUserData)

@app.route('/user/', methods=['POST'])
def create_user():

	data = request.get_json()

	hashed_password = generate_password_hash(data['password']) # Automatic salt
	new_user = User(name=data['name'], password=hashed_password, admin=False)
	userDict = new_user.convertToDict()
	userCol.insert_one(userDict)

	return jsonify({"message" : "New user created!"})

@app.route('/login/', methods=['POST'])
def login():
	auth = request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	user = userCol.find({"name": auth.username})
	if(not list(user)):
		return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	user.rewind()	
	userDict = user.next()
	
	if not userDict:
		return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	if check_password_hash(userDict.get('password'), auth.password):
		token = jwt.encode({'public_id' : userDict.get('public_id'), 'iat' : datetime.datetime.utcnow(), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

		return jsonify({'token' : token.decode('UTF-8')})
	
	return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/logout/', methods=['POST'])
@token_required
def logout(current_user):

	# TODO: Implement

	return jsonify({'message' : 'Logged out!'}), 200

if __name__ == '__main__':
	
	app.run(debug=True)