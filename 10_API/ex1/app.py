from flask import Flask, render_template, url_for, request, redirect, json, jsonify
from datetime import datetime

app = Flask(__name__) #__name__ = filename


def convert_to_dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  This dict representation includes meta data such as the object's module and class names.
  """
  
  #  Populate the dictionary with object meta data 
  obj_dict = {
    "__class__": obj.__class__.__name__,
    "__module__": obj.__module__
  }
  
  #  Populate the dictionary with object properties
  obj_dict.update(obj.__dict__)
  
  return obj_dict


class Data:
   'Common base class for all data'
   nextId = 0

   def __init__(self,temperature, humidity, pressure):
      self.temperature = temperature
      self.humidity = humidity
      self.pressure = pressure
      self.id = Data.nextId
      Data.nextId += 1
      currentDateTime = datetime.now()
      self.dateTime = currentDateTime.strftime("%Y-%m-%dT%H:%M:%S")


@app.route('/', methods=['POST', 'GET']) #root directory. POST and GET defines that the directory accepts POST and GET requests
def index():
    if request.method == 'POST':
        new_temperature = request.form['temperature']
        new_humidity = request.form['humidity']
        new_pressure = request.form['pressure']
    
        try:
            new_data = Data(temperature=new_temperature, humidity=new_humidity, pressure=new_pressure)    
            new_data_dict = convert_to_dict(new_data)

            
            with open('data.json') as json_file:
                data = json.load(json_file) # Load the current data
                temp = data['data'] # Go into the array (see JSON structure)
                temp.append(new_data_dict) # Add our new object

            with open('data.json', 'w') as json_file: #Write data (the variable from before) to the json file.
                json.dump(data, json_file, indent=4)

            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else: #Get request
        with open('data.json') as json_file:
            # Read the string
            readStr = json.load(json_file)
            
            # Form a json response and send it
            response = app.response_class(
                response=json.dumps(readStr),
                status=200,
                mimetype='application/json'
            )
            return response

if __name__ == "__main__":
    app.run(debug=True)