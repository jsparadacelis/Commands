from app.main import db


class Task(db.Document):
    command = db.StringField(max_length=60, required=True)
    started = db.BooleanField(default=False)
    output = db.StringField(default=None)
