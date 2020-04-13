import json
from pymongo import MongoClient, DESCENDING # Descending is used as a sort() specifier 
from pprint import pprint

testServerStatus = False
testDbStatus = False
testCollectionNames = False
testCursor = False
testCount = False
testFilters = False
testProjections = False
testSort = False
testRenameCollection = False
testAggregation = False
testLimitAndSkip = False
testInsertAndDelete = True

# DB config:
with open("config/db_config.json") as json_file:
    dbData = json.load(json_file)

client = MongoClient(dbData['MONGO_DB_CONNECTION_STRING'])
with client:
    db = client.pymongoTestDB # Only look at pymongoTestDB

    if(testServerStatus):
        print("Server status:")
        status = db.command("serverStatus")
        pprint(status)
        print("\n")

    if(testDbStatus):
        print("Database status:")
        status = db.command("dbstats")
        pprint(status)
        print("\n")
    
    if(testCollectionNames):
        print("Collection names:")
        print(db.list_collection_names())
        print("\n")

    # Remove collection example:
    #db.CollectionName.drop()

    if(testCursor):
        cursor = db.pymongoTest.find()
        print(cursor.next()) # Set cursor from index 0 to index 1
        print(cursor.next()) # Set cursor from index 1 to index 2
        # print(cursor.next()) # If collection only had 2 documents, this would result an error
        cursor.rewind() # Reset cursor to index 0

        print(list(cursor)) # Prints all the documents and puts cursor at last index
        cursor.rewind()

    if(testCount):
        amountOfDocuments = db.pymongoTest.count_documents({})
        print(f"There are {amountOfDocuments} documents in the collection overall")

        amountOfDocuments = db.pymongoTest.count_documents({"temperature": 0})
        print(f"There are {amountOfDocuments} documents in the collection with a temperature of 0")

    if(testFilters):
        # Using MongoDB range queries:

        # Find temperatures less than 10
        cold = db.pymongoTest.find({"temperature": {"$lt": 10}})
        
        #hot = db.pymongoTest.find({"temperature":{"$gt": 10}}) # If you wanted greather than instead

        print("Cold times:")
        for data in cold:
            print(data['dateTime'])

        amountOfColdDocuments = db.pymongoTest.count_documents({"temperature": {"$lt": 10}})
        print(f"There are {amountOfColdDocuments} documents in the collection with a temperature less than 10")

    if(testProjections):
        # Projections are used to specify what you want to see
        # You can either include data or exclude it, but not both.

        print("Printing ID, dateTime and temperature for all the data:")
        data = db.pymongoTest.find({}, {"dateTime": 1, "temperature": 1}) # NB _id is still included in this
        for i in data:
            print(i)

        #data = db.pymongoTest.find({}, {"_id": 0, "dateTime": 1, "temperature": 1}) ILLEGAL
        
        print("\nPrinting the data, excluding ID and humidity:")
        data = db.pymongoTest.find({}, {"_id": 0, "humidity": 0}) # Exclude id and humidity
        for i in data:
            print(i)

    if(testSort):
        data = db.pymongoTest.find().sort("pressure", DESCENDING) # This doesnt sort the db itself
        for i in data:
            print(i)

    if(testRenameCollection):
        #db.pymongoTest.rename('newName') # Renames collection pymongoTest to newName. Beware, this will make the other commands unable to run
        pass

    if(testAggregation):
        # Can be used for so much!

        # First argument is our group specifier. id: 1 means all the data
        # Second is what we wish to calculate
        agr = [{'$group': {'_id': 1, 'temperature': {'$sum': '$temperature'}}}] # Basically our pattern

        # Get the data        
        val = list(db.pymongoTest.aggregate(agr))
        print("Data object:")
        print(val)
        sumOfTemp = val[0]['temperature'] # This weird syntax because the object return is a list of dicts. So list index 0 and dict index 'temperature'
        print(f"The sum of all the temperatures are: {sumOfTemp}")

        # A more complex example:
        print("\nLooking at documents with a temperature of 50 or 20 degrees:")

        # More complex aggregation:
        # First find a match for all the documents with a temperature of 50 or 20.
        # Then put them in a group and make a combined object of them
        agr = [{'$match': {'$or': [ { 'temperature': 50 }, { 'temperature': 20 }] }}, 
        {'$group': {'_id': 1, 'temperature': { '$sum': "$temperature" }}}]

        val = list(db.pymongoTest.aggregate(agr))
        print("Data object (sum of all documents with temp of 50 or 20):")
        print(val)

    if(testLimitAndSkip):
        cursor = db.pymongoTest.find().skip(1).limit(2) # Skip the first document and limit the query to a maximum of 2 documents
        for i in cursor:
            print(i)
    
    if(testInsertAndDelete):
        # data to isnter
        data = {"dateTime": "2020-03-29T17:10:30",
                "humidity": 10, "pressure": 0, "temperature": -5}
        # Insert it into the colletion, returns a "pymongo.results.InsertOneResult" object.
        id = db.pymongoTest.insert_one(data)

        id = id.inserted_id # returns the actual bson ObjectID

        obj = db.pymongoTest.find_one({"_id": id}) # Find the object to print it
        print(obj)
        
        db.pymongoTest.delete_one({'_id': id}) # Delete it
        print("Deleted the object again")