from flask_restplus import Api,Resource,fields
from flask import request,make_response
from app.utils import myConverter
import json
from .. import db
from ..models import Todo
from . import bp

api = Api(app=bp,doc='/docs',
            title='Todos manager',
            description='A Todo management system')


todos = api.namespace('todos',description='Todo CRUD Operations')

todoOptions = {
                'title': fields.String(required=True,description='title of todo'),
                'content': fields.String(required=True,description='Content of todo')
            }

model = api.model(name='todo options', model= todoOptions)

# This allows datetime objects to be json serializable
@api.representation('application/json')
def output_json(data,code,headers=None):
    resp = make_response(json.dumps(data,default=myConverter),code)
    resp.headers.extend(headers or {})
    return resp

@todos.route('/')
class TodoList(Resource):
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    def get(self): # get all todos
        try:
            todo=Todo.query.all()
            if (not todo):
                todos.abort(400)
            return [tasks.serialize() for tasks in todo]
        except Exception as err:
            todos.abort(400,err.__doc__)


    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    @api.expect(model)
    def post(self): # posts a new todo
        try:
            title=request.json.get('title')
            content=request.json.get('content')
            todo=Todo(title=title,content=content)
            todo.save()
            return {
                    'status': 'ok',
                    'id': todo.id,
                    'title': todo.title,
                    'dateCreated': todo.dateCreated
                    }
        except Exception as err:
            db.session.rollback()
            todos.abort(400,err.__doc__)
            
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    def delete(self): # deletes all todos
        try:
            todo=Todo.query.all()
            if (not todo):
                todos.abort(400)
            for doc in todo:
                doc.delete()
            return {
                'status': 'ok',
                'message': 'All records successfully deleted'
            }
        except Exception as err:
            todos.abort(400,err.__doc__)

@todos.route('/<int:id>')
class Todos(Resource):
    def get(self,id): # get a particular todo
        try:
            todo=Todo.query.filter_by(id=id).first()
            if (not todo):
                todos.abort(400)
            return todo.serialize()
        
        except Exception as err:
	        todos.abort(400,err.__doc__)

    
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'},
            params={'id':'Specify user id'})
    @api.expect(model)
    def put(self,id): # updates a todo
        try:
            todo = Todo.query.filter_by(id=id).first()
            if (not todo):
                todos.abort(400)
            todo.title = request.json.get('title')
            todo.content = request.json.get('content')
            todo.save()
            return {
                    'status': 'ok',
                    'id': todo.id,
                    'title': todo.title,
                    'dateCreated': todo.dateCreated,
                    'dateModified': todo.dateModified
                    }
        
        except Exception as err:
            db.session.rollback()
            todos.abort(400,err.__doc__)


    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'},
            params={'id':'Specify user id'})
    @api.expect(model)
    def delete(self,id): # deletes a todo
        try:
            todo = Todo.query.filter_by(id=id).first()
            if (not todo):
                todos.abort(400)
            todo.delete()
            return {
                "status": 'ok',
                "message": f"record {id} successfully deleted"
            }
        except Exception as err:
            db.session.rollback()
            todos.abort(400,err.__doc__)

