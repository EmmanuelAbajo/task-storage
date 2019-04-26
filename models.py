"""Database creation for the todo API.
    The databse engine used is postgresql. The ORM used is SQLAlchemy.
    The todo table contains an id, a title  column and a content column"""

from app import db

class Todo(db.Model):
    __tablename__ = 'todo-list'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(64), unique=True, index=True, nullable=False)
    content = db.Column(db.Text, unique=True, nullable=False)
    #date_created = db.Column(db.DateTime, unique=True, nullable=False)

    def __init__(self,title,content):
        self.title = title
        self.content = content
        #self.date_created = date_created

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }

    def __repr__(self):
        return '<Todo: {}>'.format(self.title)
