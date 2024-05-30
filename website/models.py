from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	# password should never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long, depending on your hashing algorithm
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    location = db.Column(db.String(100))
    datetime =  db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    # ... Create the Comments db.relationship
	# relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
	
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))

class Order(db.Model):
    __tablename__ = 'order'
    #booking id
    id = db.Column(db.Integer, primary_key=True)
    #no of tickets
    tickets = db.Column(db.Integer)
    #user id
    #event id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))