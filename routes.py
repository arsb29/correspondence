import aiohttp_jinja2
import re
from aiohttp import web
from jinja2 import FileSystemLoader
from aiohttp_session import get_session
from auth.views import redirect, login, signUp, SignOut
from components.helpers import convert_a
from forms.ChatForm import ChatForm
from models.queries import create_chat, create_user_chat, get_user_chats, get_chat_info, chat_owner, get_chats_messages, \
    get_message_files, create_message, get_message, get_chat_users, get_not_chat_users, get_user, get_file, create_file

keysChats = ["id", "chat_id", "user_id", "needToAnswer", "title", "description", "created_date", "status"]
keysFiles = ["id", "message_id", "file"]
keysChatUsers = ["id", "login", "name", "lastName"]
keysChatMessages = ["message_id", "author_id", "name", "lastName", "avatar_file_id", "text", "created_date", "type", "reply_id", "reply_text"]


async def chats(request):
    session = await get_session(request)
    user_id = int(session.get('id'))
    if not user_id:
        redirect(request, 'login')

    payload = await request.post()
    form = ChatForm(payload)
    if request.method == 'POST' and form.validate():
        chat = await create_chat(form.title.data, form.description.data)
        await create_user_chat(chat.id, user_id)
        form.title.data = ''
        form.description.data = ''
    chats = [dict(zip(keysChats, chat)) for chat in await get_user_chats(user_id)]
    for chat in chats:
        chat['created_date'] = chat['created_date'].strftime('%Y-%m-%d в %H:%M:%S')
        if chat['status'] == 'inProgress':
            chat['status'] = 'В процессе'

    context = {'form': form, 'chats': chats}
    return aiohttp_jinja2.render_template('chats.html', request, context)


async def chat(request):
    chat_id = int(request.match_info['id'])
    session = await get_session(request)
    user_id = None
    is_chat_owner = None
    if session.get('id'):
        user_id = int(session.get('id'))
        is_chat_owner = True if await chat_owner(chat_id, user_id) else False
    chat_info = await get_chat_info(chat_id)
    messages = [dict(zip(keysChatMessages, message)) for message in await get_chats_messages(chat_id)]
    for message in messages:
        message['created_date'] = message['created_date'].strftime('%Y-%m-%d в %H:%M:%S')
        message['outcoming'] = message['author_id'] == user_id
        message['text'] = re.sub('@[a-z,0-9]*', convert_a, message['text'])
        if message['reply_text']:
            message['reply_text'] = re.sub('@[a-z,0-9]*', convert_a, message['reply_text'])
        photos = []
        files = await get_message_files(message['message_id'])
        for file in files:
            if file[4]:
                message['document_id'] = file[0]
            else:
                photos.append(file[0])
        message['photos'] = photos
    context = {'title': chat_info[1], 'messages': messages, 'is_chat_owner': is_chat_owner, 'isLogin': user_id}
    return aiohttp_jinja2.render_template('chat.html', request, context)


@aiohttp_jinja2.template('chat.html')
async def chatPost(request):
    session = await get_session(request)
    user_id = int(session.get('id'))
    chat_id = int(request.match_info['id'])
    data = await request.post()
    message = await create_message(
        chat_id=chat_id,
        user_id=user_id,
        text=data['message'],
        reply_message_id=int(data['reply_message_id']) or None,
        type='message'
    )
    if data['document'] != bytearray(b''):
        await create_file(message.id, data['document'].file.read(), data['document'].content_type, True)
    for i in range(1, int(data['countPhotos']) + 1):
        currentPhoto = data['photos' + str(i)]
        if currentPhoto != bytearray(b''):
            await create_file(message.id, currentPhoto.file.read(), currentPhoto.content_type, False)

    newMessage = dict(zip(keysChatMessages, (await get_message(message.id))[0]))
    newMessage['created_date'] = newMessage['created_date'].strftime('%Y-%m-%d в %H:%M:%S')
    newMessage['text'] = re.sub('@[a-z,0-9]*', convert_a, newMessage['text'])
    if newMessage['reply_text']:
        newMessage['reply_text'] = re.sub('@[a-z,0-9]*', convert_a, newMessage['reply_text'])
    photos = []
    files = await get_message_files(newMessage['message_id'])
    for file in files:
        if file[4]:
            newMessage['document_id'] = file[0]
        else:
            photos.append(file[0])
    newMessage['photos'] = photos

    context = {'message': newMessage}
    return web.json_response(context)


async def chatUsers(request):
    chat_id = int(request.match_info['id'])
    chat_users = [dict(zip(keysChatUsers, user)) for user in await get_chat_users(chat_id)]
    not_chat_users = [dict(zip(keysChatUsers, user)) for user in await get_not_chat_users(chat_id)]
    context = {'chat_users': chat_users, 'not_chat_users': not_chat_users}
    return web.json_response(context)


async def chatUsersPost(request):
    chat_id = int(request.match_info['id'])
    session = await get_session(request)
    user_id = int(session.get('id'))
    data = await request.post()
    login = data['login']
    user = await get_user(login)
    await create_user_chat(chat_id, user[0])
    message = '@' + login + ' добавлен'
    await create_message(
        chat_id=chat_id,
        user_id=user_id,
        text=message,
        reply_message_id=None,
        type='notify'
    )
    context = {'message': re.sub('@[a-z,0-9]*', convert_a, message)}
    return web.json_response(context)


async def file(request):
    file_id = int(request.match_info['id'])
    result = await get_file(file_id)
    return web.Response(body=result[2], content_type=result[3])


async def index(request):
    session = await get_session(request)
    if not session.get('id'):
        redirect(request, 'login')
    return await chats(request)


routes = [
    web.get('/', index, name='main'),
    web.post('/', index, name='mainPost'),
    web.get('/chat/{id:\d+}', chat, name='chat'),
    web.post('/chat/{id:\d+}', chatPost, name='chatPost'),
    web.get('/file/{id:\d+}', file, name='file'),
    web.get('/chat/{id:\d+}/users', chatUsers, name='chatUsers'),
    web.post('/chat/{id:\d+}/users', chatUsersPost, name='chatUsersPost'),
    web.get('/login', login, name='login'),
    web.post('/login', login, name='loginPost'),
    web.get('/signup', signUp, name='signup'),
    web.post('/signup', signUp, name='signupPost'),
    web.get('/signout', SignOut, name='signout'),
    web.post('/signout', SignOut, name='signoutPost')
]


def setup_routes(app):
    aiohttp_jinja2.setup(app, loader=FileSystemLoader('./templates'))
    app.add_routes(routes)
    app.router.add_static('/static', 'static', name='static')
