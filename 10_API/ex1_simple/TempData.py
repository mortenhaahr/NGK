from datetime import datetime

class TempData:
#Common base class for all data

    def __init__(self,temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        currentDateTime = datetime.now()
        self.dateTime = currentDateTime.strftime("%Y-%m-%dT%H:%M:%S")

    def convertToDict(self):
        # A function takes in a custom object and returns a dictionary representation of the object.
        # This dict representation includes meta data such as the object's module and class names.
        objDict = {}
        #  Populate the dictionary with object properties
        objDict.update(self.__dict__)

        return objDict