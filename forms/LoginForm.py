from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    login = StringField("Логин", validators=[DataRequired()], description={"placeholder": "Логин", "id": "login"})
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100)], description={"placeholder": "Пароль", "id": "password"})
    submit = SubmitField('Войти')
