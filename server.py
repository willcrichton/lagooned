from flask import Flask, session, redirect, url_for, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sockets import Sockets
from geventwebsocket import WebSocketError
from actions import ACTIONS, sanitize_action
import hashlib, uuid
import jwt
import json
import threading

# User: health/hunger, items, actions taken, island resources, explored parts
# Actions: time, callback (includes randomness), name, can_run, category
# Events: text, userID
# Item: name

# Flask/SQLAlchemy/Restful configuration options
app = Flask(__name__)
app.secret_key = 'trololololololololololol' # ultra secure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

def phash(pwd):
    return hashlib.sha512(pwd + app.secret_key).hexdigest()

def tokenize(token):
    return jwt.encode({'id': token}, app.secret_key)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    hunger = db.Column(db.Integer, default=10)
    actions = db.Column(db.Text, default=json.dumps([]))
    log = db.Column(db.Text, default=json.dumps([]))

    def json(self):
        return {
            'id'      : self.id,
            'name'    : self.name,
            'hunger'  : self.hunger,
            'token'   : tokenize(self.id),
            'actions' : json.loads(self.actions),
            'log'     : json.loads(self.log)
        }

    def valid_actions(self):
        return [a for a in ACTIONS if a['verify'](self)]
        
    def done_action(self, action):
        return action in json.loads(self.actions)

    def add_to_log(self, message):
        log = json.loads(self.log) if self.log is not None else []
        log.append(message)
        self.log = json.dumps(log)

sockets = Sockets(app)

@sockets.route('/socket')
def socket(ws):
    def GET(data, uid):
        if (data['className'] == 'User'):
            
            # if they're trying to login: validate
            if (data['model']['login']):
                try:
                    password = phash(data['model']['password'])
                    user = User.query.filter_by(name=data['model']['name'], password=password).first()
                    return user.json()
                except:
                    return {}

            # if they're already logged in: go by user id from token
            else:
                user = User.query.filter_by(id=uid).first()
                if user is None: return {}
                return user.json()

        elif (data['className'] == 'Action'):
            user = User.query.filter_by(id=uid).first()
            if user is None: return []

            return map(sanitize_action, user.valid_actions())

        
    def POST(data, uid):
        if (data['className'] == 'User'):

            # create new User instance and save it in DB
            user = User()
            user.name = data['model']['name']
            user.password = phash(data['model']['password'])
            user.add_to_log("Testing start message")

            db.session.add(user)
            db.session.commit()

            return user.json()

    def ACTION(data, uid):            
        user = User.query.filter_by(id=uid).first()
        if user is None: return {}

        action = next(a for a in ACTIONS if a['name'] == data['action'])
        if (not action['verify'](user)): return {}

        def callback():
            success = action['callback'](user)

            if success:
                completed_actions = json.loads(user.actions)
                if not action['name'] in completed_actions:
                    completed_actions.append(action['name'])

                user.actions = json.dumps(completed_actions)

            # save user model to database
            db.session.merge(user)
            db.session.commit()

            # send new user state to frontend
            ws.send(json.dumps({
                'user': user.json(),
                'actions': map(sanitize_action, user.valid_actions())
            }))
            
        threading.Timer(action['duration'], callback).start()
        return {'success': True}
            
    while True:
        try:
            message = ws.receive()
            data = json.loads(message)
            uid = jwt.decode(data['token'], app.secret_key)['id']
        except WebSocketError:
            return
        except:
            continue

        funcs = {
            'read': GET,
            'create': POST,
            'action': ACTION
        }

        to_send = funcs[data['method']](data, uid)
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
