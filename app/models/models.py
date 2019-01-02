from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy.orm.attributes import instance_state
from datetime import datetime
import uuid

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __init__(self, username, password, id=None):
        if id == None:
            id = uuid.uuid4().hex
        self.id = id
        self.username = username
        self.password = password
        self.createdAt = datetime.now()


class List(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    userId = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime)
    name = db.Column(db.String(100))

    def __init__(self, userId, name, id=None):
        if id == None:
            id = uuid.uuid4().hex
        self.id = id
        self.userId = userId
        self.createdAt = datetime.now()
        self.name = name


class Item(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    listId = db.Column(db.String(100))
    value = db.Column(db.String(120))
    createdAt = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, listId, value, id=None):
        if id == None:
            id = uuid.uuid4().hex
        self.id = id
        self.listId = listId
        self.value = value
        self.createdAt = datetime.now()


# @event.listens_for(User, 'before_update')
# def receive_modified(mapper, connection, target):
#     print instance_state(target)
#     if instance_state(target).modified:
#         target.updatedAt = datetime.now()
