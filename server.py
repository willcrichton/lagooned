from flask import Flask, session, redirect, url_for, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sockets import Sockets
from geventwebsocket import WebSocketError
from actions import ACTIONS, sanitize_action
from messages import M
import hashlib, uuid
import jwt
import json
import threading
import time

# User: health/hunger, items, actions taken, island resources, explored parts
# Actions: time, callback (includes randomness), name, can_run, category
# Events: text, userID
# Item: name

# Flask/SQLAlchemy/Restful configuration options
app = Flask(__name__)
app.secret_key = 'trololololololololololol' # ultra secure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

# password hashing function
def phash(pwd):
    return hashlib.sha512(pwd + app.secret_key).hexdigest()

# encode input as JSON web token
def tokenize(token):
    return jwt.encode({'id': token}, app.secret_key)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    hunger = db.Column(db.Integer, default=10)
    completed = db.Column(db.Text, default="[]")
    current_action = db.Column(db.Text, default="{}")
    log = db.Column(db.Text, default="[]")
    items = db.Column(db.Text, default="{}")

    def json(self):
        return {
            'id'        : self.id,
            'name'      : self.name,
            'hunger'    : self.hunger,
            'token'     : tokenize(self.id),
            'completed' : json.loads(self.completed),
            'log'       : [M[v] for v in json.loads(self.log)],
            'current_action' : self.get_current_action(),
            'items'     : {M[k]: v for k,v in self.get_items().items()}
        }

    # Potential actions
    def valid_actions(self):
        return [a for a in ACTIONS if a['verify'](self)]
    
    # Completed actions
    def done_actions(self, actions):
        completed = json.loads(self.completed)
        for action in actions:
            if not action in completed: return False
        return True

    # Event log
    def add_to_log(self, message):
        log = json.loads(self.log) if self.log is not None else []
        log.append(message)
        self.log = json.dumps(log)

    # Current actions
    def set_current_action(self, action):
        current_action = sanitize_action(action)
        current_action['start'] = time.time()
        self.current_action = json.dumps(current_action)

    def get_current_action(self):
        return json.loads(self.current_action)

    def can_act(self):
        current_action = self.get_current_action()
        if not 'start' in current_action: return True
        return time.time() - current_action['start'] >= current_action['duration']

    # Inventory
    def get_items(self):
        return json.loads(self.items)

    def has_item(self, item, qty=1):
        items = self.get_items()
        if not item in items: return False
        return items[item] >= qty

    def add_item(self, item):
        items = self.get_items()
        if not item in items: items[item] = 0
        items[item] += 1
        self.items = json.dumps(items)

    def remove_item(self, item, qty=1):
        items = self.get_items()
        items[item] -= qty
        self.items = json.dumps(items)

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
            user.add_to_log('GAME_START')

            db.session.add(user)
            db.session.commit()

            return user.json()

    def ACTION(data, uid):            
        user = User.query.filter_by(id=uid).first()
        if user is None: return {}

        action = next(a for a in ACTIONS if a['name'] == data['action'])
        if (not action['verify'](user) or not user.can_act()): return {'success': False}

        def callback():
            success = action['callback'](user)

            if success:
                completed_actions = json.loads(user.completed)
                if not action['name'] in completed_actions:
                    completed_actions.append(action['name'])

                user.completed = json.dumps(completed_actions)

            # save user model to database
            db.session.merge(user)
            db.session.commit()

            # send new user state to frontend
            ws.send(json.dumps({
                'user': user.json(),
                'actions': map(sanitize_action, user.valid_actions())
            }))

        user.set_current_action(action)
        db.session.merge(user)
        db.session.commit()

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
