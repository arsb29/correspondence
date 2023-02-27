from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(Form):
    title = StringField("Название", validators=[DataRequired()], description={"placeholder": "Название", "id": "title"})
    description = StringField("Описание", description={"placeholder": "Описание", "id": "description"})
    submit = SubmitField('Войти')



