from mongoengine import Document, StringField, IntField


class User(Document):
    name = StringField()
    username = StringField()
    wallet = IntField(max_value=0, default=0)
    
