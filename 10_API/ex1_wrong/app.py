from flask import Flask, render_template, url_for, request, redirect, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #__name__ = filename
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 forward slashes for relative path
db = SQLAlchemy(app) # Pass in app to database and init db

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

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer)#, nullable=False) #Max 200 chars and dont allow it to be blank
    date = db.Column(db.DateTime, default=datetime.utcnow) #Never has to be set manually
    humidity = db.Column(db.Integer)#, nullable=False)
    pressure = db.Column(db.Integer)#, nullable=False)

    # Everytime we make a data taks, it shall return the ID of that task:
    def __repr__(self):
        print("Hej")
        return convert_to_dict(self)
    def __str__(self):
        #thisdict = {
        #    "id": self.id,
        #    "date": self.date,
        #    "temperature": self.temperature,
        #    "humidity": self.humidity,
        #    "pressure": self.pressure
        #}
        #return json.dumps(thisdict)
        return convert_to_dict(self)
   

@app.route('/', methods=['POST', 'GET']) #root directory. POST and GET defines that the directory accepts POST and GET requests
def index():
    if request.method == 'POST':
        task_temperature = request.form['temperature']
        task_humidity = request.form['humidity']
        task_pressure = request.form['pressure']
    
        try:
            new_task = Data(temperature=task_temperature, humidity=task_humidity, pressure=task_pressure)    
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else: #Get request
        tasks = Data.query.order_by(Data.date).all() # Return all database instances in order created
        
        return "Hello world"#json.dumps(dictTasks)

if __name__ == "__main__":
    app.run(debug=True)