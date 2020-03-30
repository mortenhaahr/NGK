from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #__name__ = filename
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 forward slashes for relative path
db = SQLAlchemy(app) # Pass in app to database and init db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) #Max 200 chars and dont allow it to be blank
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #Never has to be set manually

    # Everytime we make a new taks, it shall return the ID of that task:
    def __repr__(self):
        return '<Task %r' % self.id
    
    #Must setup database manually in python ONCE, to create the db in env:
    # Type following in console:
    # python3 [enter] from app import db [enter] db.create_all() [enter] exit() [enter]

@app.route('/', methods=['POST', 'GET']) #root directory. POST and GET defines that the directory accepts POST and GET requests
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # Return all database instances in order created
        #return "Hello, World!" # return basic string on website
        return render_template('index.html', tasks=tasks) #return index page.

# make delete route
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # Get object by id, if it fails, throw 404

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id) #define our task variable for this function

    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)