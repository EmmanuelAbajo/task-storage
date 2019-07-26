from datetime import datetime as dt
from flask_restplus import Namespace,fields

def myConverter(obj):
        if isinstance(obj,dt):
            return obj.__str__()

class TodoDTO:
    api = Namespace('todos',description='Todo CRUD Operations')
    todoOptions = {
                'title': fields.String(required=True,description='title of todo'),
                'content': fields.String(required=True,description='Content of todo')
            }
    todoModel = api.model(name='todo options', model= todoOptions)

class UserDTO:
    api = Namespace('users',description='user management')
    userOptions = {
                'username': fields.String(required=True,description='username'),
                'password': fields.String(required=True,description='password')
            }
    userModel = api.model(name='userModel', model= userOptions)
