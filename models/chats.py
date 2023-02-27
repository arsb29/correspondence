from models import db


class Chats(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Text, nullable=False)
