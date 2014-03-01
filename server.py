from flask import Flask, session, redirect, url_for, render_template, request
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sockets import Sockets
import json

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
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    hunger = db.Column(db.Integer, default=10)

# User rest model is a little different in that although we have a 
# collection of Users, any one User should only be able to access 
# his/her own data.
class UserRest(Resource):
    def get(self):
        if not 'id' in session: return {}

        # User can only access his own data
        user = User.query.filter_by(id=session['id']).first()
        return {
            'id'   : user.id,
            'name' : user.name
        }

    def post(self):
        if 'id' in session: return

        # retrieve parameters from POST request
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='User\'s name')
        args = parser.parse_args()

        # create new User instance and save it in DB
        user = User()
        user.name = args['name']
        db.session.add(user)
        db.session.commit()
        
        # save a cookie of user's id
        # TODO: password authentication
        session['id'] = user.id
        return {'id': user.id}
        

api.add_resource(UserRest, '/api/user')

sockets = Sockets(app)

@sockets.route('/socket')
def socket(ws):
    while True:
        message = ws.receive()
        print message
        ws.send(message)

@app.route('/api/action')
def action():
    print request.args
    return ''

@app.route('/')
def index():
    return render_template('index.jinja2', logged_in=json.dumps('id' in session))

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    #WSGIServer(('', 5000), app, handler_class=WebSocketHandler).serve_forever()
