from . import db

class Todo(db.Model):
    __tablename__ = 'todo-list'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(64), index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    dateCreated = db.Column(db.DateTime,default=db.func.current_timestamp())
    dateModified = db.Column(db.DateTime,default=db.func.current_timestamp(),\
                                        onupdate=db.func.current_timestamp())

    def __init__(self,title,content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Todo: {}>'.format(self.title)


    def serialize(self):
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'dateCreated': self.dateCreated
        }
        if self.dateCreated != self.dateModified:
            data.update('dateModified',self.dateModified)

        return data
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

