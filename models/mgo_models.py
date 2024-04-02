from mongoengine import Document, StringField, IntField, BooleanField, ListField, ReferenceField


class User(Document):
    telegram_id = IntField(required=True, unique=True)
    full_name = StringField()
    username = StringField()
    wallet = IntField(min_value=0, default=0)
    invites = IntField(min_value=0, default=0)
    inviter = IntField()
    is_premium = BooleanField()

    meta = {
        'collection': 'users',
        'indexes': [
            'telegram_id',
            'username'
        ]
    }


class FileDownload(Document):
    title = StringField(required=True)
    description = StringField()
    users = ListField(ReferenceField(User))
    is_active = BooleanField(default=True)
    is_downloadable = BooleanField(default=True)

    meta = {
        'collection': 'file.download',
        'indexes': [
            'title',
            'is_active',
            'is_downloadable'
        ]
    }
    
    
class UserSteps(Document):
    STEPS = (
        ("INPUT_FILE_NAME", "input file name"),
        ("INPUT_FILE_DESC", "input file description"),
        ("INPUT_FILE_APPROVE", "approve to create file"),
    )
    user = ReferenceField(User, required=True, unique=True)
    step = StringField(choices=STEPS)
    data = StringField()
    
    meta = {
        'collection': 'user.steps',
        'indexes': [
            'user',
            'step',
        ]
    }