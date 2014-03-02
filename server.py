from flask import Flask, session, redirect, url_for, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sockets import Sockets
from geventwebsocket import WebSocketError
import hashlib, uuid
import jwt
import json

# User: health/hunger, items, actions taken, island resources, explored parts
# Actions: time, callback (includes randomness), name, can_run, category
# Events: text, userID
# Item: name

class Action():
    name = ''
    dependencies = []
    time = 0

    def __init__(self, n, d, t):
        name = n
        dependencies = d
        time = t
    
ACTIONS = [
    Action('Scavenge', [], 10)
]

# Flask/SQLAlchemy/Restful configuration options
app = Flask(__name__)
app.secret_key = 'trololololololololololol' # ultra secure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    hunger = db.Column(db.Integer, default=10)

def phash(pwd):
    return hashlib.sha512(pwd + app.secret_key).hexdigest()

def tokenize(token):
    return jwt.encode({'id': token}, app.secret_key)

sockets = Sockets(app)

@sockets.route('/socket')
def socket(ws):
    def GET(data, uid):
        if (data['className'] == 'User'):
            if (data['model']['login']):
                try:
                    password = phash(data['model']['password'])
                    user = User.query.filter_by(name=data['model']['name'], password=password).first()
                    return {
                        'id'   : user.id,
                        'name' : user.name,
                        'token': tokenize(user.id)
                    }
                except:
                    return {}
            else:
                user = User.query.filter_by(id=uid).first()
                return {
                    'id'   : user.id,
                    'name' : user.name,
                    'token': tokenize(user.id)
                }

    def POST(data, uid):
        if (data['className'] == 'User'):

            # create new User instance and save it in DB
            user = User()
            user.name = data['model']['name']
            user.password = phash(data['model']['password'])
            db.session.add(user)
            db.session.commit()
        
            return {
                'id'   : user.id,
                'name' : user.name,
                'token': tokenize(user.id)
            }
            
    while True:
        try:
            message = ws.receive()
            data = json.loads(message)
            uid = jwt.decode(data['token'], app.secret_key)['id']
        except WebSocketError:
            break;
        except:
            continue

        if data['method'] == 'read':
            to_send = GET(data, uid)
        elif data['method'] == 'create':
            to_send = POST(data, uid)

        ws.send(json.dumps(to_send))


@app.route('/')
def index():
    uid = session['id'] if 'id' in session else ''
    return render_template('index.jinja2', token=tokenize(uid))

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
