from flask import Flask, render_template, url_for, request, redirect, json, jsonify
from datetime import datetime
from TempData import TempData

app = Flask(__name__) #__name__ = filename

@app.route('/', methods=['POST', 'GET']) #root directory. POST and GET defines that the directory accepts POST and GET requests
def index():
    if request.method == 'POST':
        new_temperature = request.form['temperature']
        new_humidity = request.form['humidity']
        new_pressure = request.form['pressure']
    
        try:
            new_data = TempData(temperature=new_temperature, humidity=new_humidity, pressure=new_pressure)    
            new_data_dict = new_data.convertToDict()
            
            
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