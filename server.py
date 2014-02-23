from flask import Flask, session, redirect, url_for, render_template, request
from flask.ext.restful import Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.secret_key = 'trololololololololololol'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class UserRest(Resource):
    def get(self):
        if not 'id' in session: return {}
        
        user = User.query.filter_by(id=session['id']).first()
        return {
            'name': user.name
        }

    def post(self):
        if 'id' in session: return
        
        user = User()
        db.session.add(user)
        db.session.commit()
        
        session['id'] = user.id
        

api.add_resource(UserRest, '/api/user/')

@app.route('/')
def index():
    return render_template('index.jinja2', logged_in=json.dumps('id' in session))


if __name__ == '__main__':
    app.run(debug=True)
