from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from config import config
import os


app = Flask(__name__)

## Configuration
#app.config.from_object(config['development'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

from models import Todo

@app.route("/get/<int:id_>",methods=['GET'])
def get_by_id(id_):
    try:
        todo=Todo.query.filter_by(id=id_).first()
        return jsonify(todo.serialize())
    except Exception as e:
	    return jsonify({'Error': str(e)})

@app.route("/getall",methods=['GET'])
def get_all():
    try:
        todo=Todo.query.all()
        return jsonify([tasks.serialize() for tasks in todo])
    except Exception as e:
	    return jsonify({'Error': str(e)})

# For url query parameters, we use request.args
# For form input, we use request.form
@app.route("/add",methods=['POST','GET'])
def add_book():
    title=request.form.get('title')
    content=request.form.get('content')
    try:
        todo=Todo(title=title,content=content)
        db.session.add(todo)
        db.session.commit()
        return "Todo added. todo id={}".format(todo.id)
    except Exception as e:
           return jsonify({'Error': str(e)})

## TODO: Add client side functionality for add end point
# - Validate both inputs
# - Store form data in user sessions'
# - redirect to add endpoint
# - render homepage.html template

if __name__ == '__main__':
    app.run()
