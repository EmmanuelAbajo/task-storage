from flask_restplus import Api,Resource,abort
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request
from .. import db
from models.model import Todo
from app.utils import TodoDTO

api = TodoDTO.api #namespace
model = TodoDTO.todoModel

@api.route('/')
class TodoList(Resource):
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    @jwt_required
    def get(self): # get all todos
        try:
            todo=Todo.query.filter_by(created_by=get_jwt_identity())
            if not todo:
                return {"message":"No todos found"}
            
            return [tasks.serialize() for tasks in todo]
        except Exception as err:
            abort(400,message=err)


    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    @api.expect(model,validate=True)
    @jwt_required
    def post(self): # posts a new todo
        try:
            title=request.json.get('title')
            content=request.json.get('content')
            created_by = get_jwt_identity()
            todo=Todo(title=title,content=content,created_by=created_by)
            todo.save()
            return {
                    'status': 'ok',
                    'id': todo.id,
                    'title': todo.title,
                    'dateCreated': todo.dateCreated
                    }
        except Exception as err:
            db.session.rollback()
            abort(400,err)
            
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    @jwt_required
    def delete(self): # deletes all todos
        try:
            todo=Todo.query.filter_by(created_by=get_jwt_identity())
            if not todo:
                return {"message":"No todos found"}
            for doc in todo:
                doc.delete()
            return {
                'status': 'ok',
                'message': 'All records successfully deleted'
            }
        except Exception as err:
            abort(400,message=err)


@api.route('/<int:id>')
class Todos(Resource):
    @jwt_required
    def get(self,id): # get a particular todo
        try:
            todo=Todo.query.filter_by(created_by=get_jwt_identity(),id=id).first()
            if not todo:
                return {"message":"todo not found"}
            return todo.serialize()
        
        except Exception as err:
            print(err)
            abort(400,err)

    
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'},
            params={'id':'Specify user id'})
    @api.expect(model,validate=True)
    @jwt_required
    def put(self,id): # updates a todo
        try:
            todo = Todo.query.filter_by(created_by=get_jwt_identity(),id=id).first()
            if not todo:
                return {"message":"todo not found"}
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
            abort(400,err)


    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'},
            params={'id':'Specify user id'})
    @api.expect(model)
    @jwt_required
    def delete(self,id): # deletes a todo
        try:
            todo = Todo.query.filter_by(created_by=get_jwt_identity(),id=id).first()
            if not todo:
                return {"message":"todo not found"}
            todo.delete()
            return {
                "status": 'ok',
                "message": f"record {id} successfully deleted"
            }
        except Exception as err:
            db.session.rollback()
            abort(400,err)

