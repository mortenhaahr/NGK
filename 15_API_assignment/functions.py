def convertObjectId(id):
    if(isinstance(id, list)):
        try:
            for i in id: # Convert the bson ObjectID (which is default from mongodb) to strings, so json.dumps can handle them
                i['_id'] = str(i['_id'])
            return id
        except:
            print("Error in convertObjectId")
            return 0
    elif(isinstance(id,dict)):
        try: # Convert the bson ObjectID (which is default from mongodb) to strings, so json.dumps can handle them
            bsonid = id.get('_id')
            strid = str(bsonid)
            id.pop('_id')
            id['_id'] = strid
            return id
        except:
            print("Error in convertObjectId")
            return 0
    else:
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