from datetime import datetime
from math import floor

class WeatherData:
#Common base class for all data

    def __init__(self, place, temperature, humidity, pressure):
        self.place = place
        self.temperature = floor(temperature*10)/10 # Round to 1 decimal
        self.humidity = str(humidity) + " %"
        self.pressure = floor(pressure*10)/10 # Round to 1 decimal
        currentDateTime = datetime.now()
        self.dateTime = currentDateTime.strftime("%Y-%m-%dT%H:%M:%S")

    def convertToDict(self):
        # A function takes in a custom object and returns a dictionary representation of the object.
        # This dict representation includes meta data such as the object's module and class names.
        objDict = {}
        #  Populate the dictionary with object properties
        objDict.update({"place": {"name": self.place.name, "lat": self.place.lat, "lon": self.place.lon}})
        objDict.update({"temp": self.temperature})
        objDict.update({"humidity": self.humidity})
        objDict.update({"press": self.pressure})
        objDict.update({"dateTime": self.dateTime})

        return objDict

class Place:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon