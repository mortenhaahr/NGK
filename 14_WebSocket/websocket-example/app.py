from flask import Flask, render_template, json
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('new user')
def new_user(msg, methods=['GET', 'POST']):
    print('New user: ' + str(json.dumps(msg)))
    socketio.emit('my response', msg, callback=messageReceived)

@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    print('received my event: ' + str(msg))
    socketio.emit('my response', msg, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)