from models import db


class Files(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, nullable=True)
    file = db.Column(db.LargeBinary, nullable=False)
    content_type = db.Column(db.Text, nullable=False)
    is_main = db.Column(db.Boolean, nullable=True)
