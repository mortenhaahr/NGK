import uuid

class User:

    def __init__(self, name, password, admin = False):
        self.name = name
        self.password = password
        self.admin = admin
        self.public_id = str(uuid.uuid4())
        
    def convertToDict(self):
        # A function takes in a custom object and returns a dictionary representation of the object.
        # This dict representation includes meta data such as the object's module and class names.
        objDict = {}
        #  Populate the dictionary with object properties
        objDict.update(self.__dict__)

        return objDict