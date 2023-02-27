import json
from time import time
import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web
from forms.LoginForm import LoginForm
from forms.SignUpForm import SignUpForm
from models.queries import check_user, create_file, create_user


def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)


def set_session(session, id, request, view_name):
    session['id'] = str(id)
    session['last_visit'] = time()
    redirect(request, view_name)


def convert_json(message):
    return json.dumps({'error': message})


async def login(request):
    session = await get_session(request)
    if session.get('id'):
        redirect(request, 'main')
    payload = await request.post()
    form = LoginForm(payload)
    if request.method == 'POST' and form.validate():
        result = await check_user(form.login.data)
        if result and result.password == form.password.data:
            session = await get_session(request)
            set_session(session, str(result.id), request, 'main')
        else:
            form.login.errors.append('Неверный пара пользователь/пароль')
    context = {'form': form}
    return aiohttp_jinja2.render_template('auth/login.html', request, context)


async def signUp(request):
    session = await get_session(request)
    if session.get('user'):
        redirect(request, 'main')
    payload = await request.post()
    form = SignUpForm(payload)
    if request.method == 'POST' and form.validate():
        result = await check_user(form.login.data)
        if result:
            form.login.errors.append('Данный пользователь уже существует')
        else:
            file = form.file.data
            avatar = None
            if file != bytearray(b''):
                avatar = await create_file(None, file.file.read(), file.content_type, False)
            result = await create_user(
                login=form.login.data,
                name=form.name.data,
                lastName=form.lastName.data,
                number=form.number.data,
                email=form.email.data,
                password=form.password.data,
                description=form.description.data,
                file_id=avatar and avatar.id
            )
            session = await get_session(request)
            set_session(session, result.id, request, 'main')

    context = {'form': form}
    return aiohttp_jinja2.render_template('auth/signup.html', request, context)


class SignOut(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('id'):
            del session['id']
        redirect(self.request, 'login')
