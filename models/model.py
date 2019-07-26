from app import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,index=True,nullable=False,unique=True)
    password = db.Column(db.String(128))
    todos = db.relationship('Todo',order_by='Todo.id',cascade="all,delete-orphan")
    # The cascade= all, delete-orphan will delete all todos when a referenced user is deleted

    def __repr__(self):
        return f"<User: {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit(self)

    @classmethod
    def findByUsername(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def getAllUsers(cls):
        def toJson(data):
            return {
                'username': data.username,
                'password': data.password
            }
        users = cls.query.all()
        if not users:
            return {"message":"No existing user"}
        return {
            'users': list(map(lambda x: toJson(x),users))
        }

    @classmethod
    def dropAllUsers(cls):
        try:
            no_of_rows = db.session.query(cls).delete()
            db.session.commit()
            if not no_of_rows:
                return {'message': 'No user in the database'}
            return {
                'message': f'{no_of_rows} user(s) deleted'
            }
        except Exception as err:
            db.session.rollback()
            return {
                'message': err
            }

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class Todo(db.Model):
    __tablename__ = 'todo-list'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(64), index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    dateCreated = db.Column(db.DateTime,default=db.func.current_timestamp())
    dateModified = db.Column(db.DateTime,default=db.func.current_timestamp(),
                                        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer,db.ForeignKey(User.id))
    
    def __init__(self,title,content,created_by):
        self.title = title
        self.content = content
        self.created_by = created_by

    def __repr__(self):
        return '<Todo: {}>'.format(self.title)


    def serialize(self):
        data = {
            'creator': self.created_by,
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'dateCreated': self.dateCreated
        }
        if self.dateCreated != self.dateModified:
            data.update({'dateModified':self.dateModified})

        return data
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

