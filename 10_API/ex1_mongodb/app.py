from flask import Flask, render_template, url_for, request, redirect, json, jsonify
from datetime import datetime
from pymongo import MongoClient, DESCENDING

import re # regular expressions used in specific date endpoint

from WeatherData import WeatherData

# DB config:
with open("config/db_config.json") as json_file:
    dbData = json.load(json_file)

app = Flask(__name__) #__name__ = filename
mongoClient = MongoClient(dbData['MONGO_DB_CONNECTION_STRING']) # load the client based on config file
mongoDb = mongoClient["NGKWeatherDB"]
mongoCol = mongoDb["WeatherData"] # mongoCollection. 

def convertObjectId(id):
    try:
        for i in id: # Convert the bson ObjectID (which is default from mongodb) to strings, so json.dumps can handle them
            i['_id'] = str(i['_id'])
        return id
    except:
        print("Error in convertObjectId")
        return 0

def isDate(datestr):
    # Checks if the date is in format: YYYYMMDD

    if(not(len(datestr) == 8)): # Make sure it has correct length
        return 0
    year = int(datestr[0:4]) # Get first 4 letters of the string and convert it to a year
    if((year > 2038) or (year < 1970)):
        return 0
    month = int(datestr[4:6]) # Get the date
    if((month > 12) or (month < 1)):
        return 0
    
    daysPrMonth = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # It is a leap year if the year is divisble by 4, but not by 100, except if it is also divisible by 400
    if (year % 4) == 0: 
        if(year % 100 == 0):
            if(year % 400 == 0):
                daysPrMonth[2] = 29
        else:
            daysPrMonth[2] = 29

    date = int(datestr[6:8])
    if((date < 1) or (date > daysPrMonth[month])):
        return 0
    # Returns 1 if it is in correct format
    return 1
    

@app.route('/', methods=['POST', 'GET']) # Post is for new data and get is for all
def index():
    if request.method == 'POST':
        new_temperature = request.form['temperature']
        new_humidity = request.form['humidity']
        new_pressure = request.form['pressure']
    
        try:
            newWeather = WeatherData(temperature=new_temperature, humidity=new_humidity, pressure=new_pressure)    
            newWeatherDict = newWeather.convertToDict()
            
            mongoCol.insert_one(newWeatherDict)

            return redirect('/')
        except:
            return 'There was an issue adding your data'
    else: #Get request
        cursor = mongoCol.find() # make cursor with no sorting
        listOfWeatherData = list(cursor) # return all the objects as a list and set the cursor to last index
        
        listOfWeatherData = convertObjectId(listOfWeatherData) # See function

        return json.dumps(listOfWeatherData)

@app.route('/latest', methods=['GET']) # Get the latest 3 datas
def latest():
    cursor = mongoCol.find().sort("dateTime", DESCENDING).limit(3) # This doesnt sort the db itself
    listOfWeatherData = list(cursor) # return all the objects as a list and set the cursor to last index

    listOfWeatherData = convertObjectId(listOfWeatherData) # See function

    return json.dumps(listOfWeatherData)

@app.route('/specific/<date>', methods=['GET']) # Get the latest 3 datas
def specific(date):
    if(isDate(date)):
        date = date[0:4] + "-" + date[4:6] + "-" + date[6:8] # Fix the formatting to be the same as db
        regex = re.compile(f'^{date}') # Regex pattern to match all with same date as ours. Ignores the time
        cursor = mongoCol.find({"dateTime": {'$regex': regex}})
        listOfWeatherData = list(cursor) # return all the objects as a list and set the cursor to last index
    
        listOfWeatherData = convertObjectId(listOfWeatherData) # See function

        return json.dumps(listOfWeatherData)
    else:
        return "Error in date. Write in format: YYYYMMDD"

if __name__ == "__main__":
    try:
        mongoClient.server_info()
    except:
        print("Error connecting to mongoDB")
        exit(1)
    app.run(debug=True)