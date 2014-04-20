from flask import Flask, session, redirect, url_for, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sockets import Sockets
from geventwebsocket import WebSocketError
from actions import ACTIONS, CONSTRAINTS, sanitize_action, on_action
from constants import C
import hashlib, uuid
import jwt
import json
import threading
import time

# User: health/hunger, items, actions taken, island resources, explored parts
# Actions: time, callback (includes randomness), name, can_run, category
# Events: text, userID
# Item: name

# Flask/SQLAlchemy/Socket configuration options
app = Flask(__name__)
app.secret_key = 'trololololololololololol' # ultra secure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)
sockets = Sockets(app)

# encode input as JSON web token
def tokenize(token):
    return jwt.encode({'id': token}, app.secret_key)

# the User class is the heart of data storage on serverside
# it uses SQLAlchemy to save all these fields to the SQLite db
# and we store literally everything on the User table (woo fat tables)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)                # unique identifier for each user
    name = db.Column(db.String(80), unique=True)                # handle that other players see
    password = db.Column(db.String(80))
    food = db.Column(db.Integer)                     # amount of food a player has
    completed = db.Column(db.Text)                # list of completed actions
    current_action = db.Column(db.Text)           # name/duration of current action
    log = db.Column(db.Text)                      # list of all messages sent to user
    items = db.Column(db.Text)                    # list of all items user has (name/qty)
    location = db.Column(db.String(80))   # current location of player

    def json(self):
        return {
            'id'        : self.id,
            'name'      : self.name,
            'food'      : self.food,
            'location'  : C[self.location],
            'token'     : tokenize(self.id),
            'completed' : json.loads(self.completed),
            'log'       : [C[v] for v in json.loads(self.log)][-C['LOG_MAX']:],
            'items'     : {C[k]: {'qty': v, 'desc': C['%s_DESC' % k]} for k,v in self.get_items().items()}
        }

    def save(self):
        db.session.merge(self)
        db.session.commit()

    # List of potential actions
    def valid_actions(self):
        return [a for a in ACTIONS if self.can_run(a)]
    
    # Check if user has done all of the given list of actions
    def has_done_actions(self, actions):
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

    # Player is busy if they're performing an action
    def is_busy(self):
        current_action = self.get_current_action()
        if not 'start' in current_action: return False
        return time.time() - current_action['start'] < current_action['duration']

    # Action is run if we can verify it AND passes all constraints
    def can_run(self, action):
        if not action['verify'](self): return False

        for callback in CONSTRAINTS:
            if not callback(self, action): return False

        return True

    # Inventory helpers
    def get_items(self):
        return json.loads(self.items)

    def has_item(self, item, qty=1):
        items = self.get_items()
        if not item in items: return False
        return items[item] >= qty

    def has_items(self, items, qty=1):
        my_items = self.get_items()
        count = 0
        for item in items:
            if not item in my_items: continue
            count += my_items[item]
        return count >= qty
    
    def add_item(self, item):
        items = self.get_items()
        if not item in items: items[item] = 0
        items[item] += 1
        self.items = json.dumps(items)

    def remove_item(self, item, qty=1):
        items = self.get_items()
        items[item] -= qty
        self.items = json.dumps(items)

    def num_of_item(self, item):
        items = self.get_items()
        return items[item] if item in items else 0

    def num_of_items(self, item_list):
        return sum([self.num_of_item(item) for item in item_list])

@sockets.route('/socket')
def socket(ws):

    # password hashing function
    def phash(pwd):
        return hashlib.sha512(pwd + app.secret_key).hexdigest()

    # retrieving data from a model
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
            
            # They want all actions the user can take
            user = User.query.filter_by(id=uid).first()
            if user is None: return []

            return map(sanitize_action, user.valid_actions())

    # creating a new model
    def POST(data, uid):
        if (data['className'] == 'User'):

            # create new User instance and save it in DB
            user = User()
            user.name = data['model']['name']
            user.password = phash(data['model']['password'])
            user.food = 5
            user.completed = '[]'
            user.current_action = '{}'
            user.log = '[]'
            user.items = '{}'
            user.location = 'LOCATION_BEACH'
            user.add_to_log('GAME_START')
            db.session.add(user)
            db.session.flush()
            db.session.commit()

            return user.json()

    # doing an action
    def ACTION(data, uid):            
        user = User.query.filter_by(id=uid).first()
        if user is None: return {}

        action = next(a for a in ACTIONS if a['name'] == data['action'])
        if (user.is_busy() or not user.can_run(action)): return {'success': False}

        def callback():
            success = action['callback'](user)

            if success:
                completed_actions = json.loads(user.completed)
                if not action['name'] in completed_actions:
                    completed_actions.append(action['name'])

                user.completed = json.dumps(completed_actions)

            on_action(user)
            user.save()

            # send new user state to frontend
            ws.send(json.dumps({
                'user': user.json(),
                'actions': map(sanitize_action, user.valid_actions())
            }))

        user.set_current_action(action)
        user.save()

        # spawn a thread to run the success callback after the action duration
        # TODO: better way to do this besides threads? what about stopping early?
        threading.Timer(action['duration'], callback).start()
        return {'success': True}

    # read from the socket as long as the connection is open
    while True:
        try:
            message = ws.receive()
            data = json.loads(message)
            uid = jwt.decode(data['token'], app.secret_key)['id']
        except WebSocketError:
            # they quit the connection, kill the socket
            return
        except:
            # miscellaneous errors (eg bad JSON), ignore the message
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
