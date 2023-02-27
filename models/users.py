from models import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, nullable=True)
    login = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    lastName = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    number = db.Column(db.Text)
    description = db.Column(db.Text)


class UsersChats(db.Model):
    __tablename__ = 'usersChats'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    needToAnswer = db.Column(db.Boolean, nullable=False)

    _table_args__ = (
        db.ForeignKeyConstraint(['chat_id'], ['chats.id'], name='UsersChats__chat_id__fk'),
        db.ForeignKeyConstraint(['user_id'], ['users.id'], name='UsersChats__user_id__fk')
    )
