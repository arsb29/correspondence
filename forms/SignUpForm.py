from wtforms import Form, StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignUpForm(Form):
    login = StringField("Логин", validators=[DataRequired()], description={"placeholder": "Логин", "id": "login"})
    name = StringField("Имя", validators=[DataRequired()], description={"placeholder": "Имя", "id": "name"})
    lastName = StringField("Фамилия", validators=[DataRequired()], description={"placeholder": "Фамилия", "id": "lastName"})
    number = StringField("Телефон", validators=[DataRequired()], description={"placeholder": "Телефон", "id": "number"})
    email = StringField("Почта", validators=[DataRequired(), Email('Некорректная почта')], description={"placeholder": "Почта", "id": "email"})
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100)], description={"placeholder": "Пароль", "id": "password"})
    password2 = PasswordField("Подтверждение пароля", validators=[
        DataRequired(),
        Length(min=4, max=100),
        EqualTo('password', 'Пароли должны совпадать')
    ], description={"placeholder": "Подтверждение пароля", "id": "password2"})
    description = StringField("О себе", validators=[DataRequired()], description={"placeholder": "О себе", "id": "description"})
    file = FileField()
    submit = SubmitField('Регистрация')
