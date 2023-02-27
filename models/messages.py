from models import db


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=False)
    reply_message_id = db.Column(db.Integer, nullable=True)
    type = db.Column(db.Text, nullable=False)

    _table_args__ = (
        db.ForeignKeyConstraint(['chat_id'], ['chats.id'], name='Messages__chat_id__fk'),
        db.ForeignKeyConstraint(['user_id'], ['users.id'], name='Messages__user_id__fk')
    )
