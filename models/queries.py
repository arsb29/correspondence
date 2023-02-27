from datetime import datetime
from models import db
from models.chats import Chats
from models.files import Files
from models.messages import Messages
from models.users import Users, UsersChats


# Chats


async def create_chat(title, description):
    result = Chats(
        title=title,
        description=description,
        created_date=datetime.today(),
        status='inProgress'
    )
    return await result.create()


async def get_chat_info(chat_id):
    query = db.text('''
        SELECT * FROM chats
        WHERE id=:chat_id
    ''')
    return await db.first(query, chat_id=chat_id)


async def chat_owner(chat_id, user_id):
    query = db.text('''
        SELECT * FROM "usersChats"
        WHERE user_id=:user_id AND chat_id=:chat_id
    ''')
    return await db.first(query, chat_id=chat_id, user_id=user_id)


async def get_chat_users(chat_id):
    query = db.text('''
        SELECT users.id, users.login, users.name, users."lastName" FROM "usersChats"
        INNER JOIN users
        ON users.id="usersChats".user_id
        WHERE chat_id=:chat_id
    ''')
    return await db.all(query, chat_id=chat_id)


async def get_not_chat_users(chat_id):
    query = db.text('''
        SELECT id, login, name, "lastName"
        FROM users WHERE id NOT IN (
            SELECT users.id as id
            FROM "usersChats"
            INNER JOIN users
            ON users.id="usersChats".user_id
            WHERE chat_id=:chat_id
        )
    ''')
    return await db.all(query, chat_id=chat_id)


# Files


async def create_file(message_id, file, content_type, is_main):
    result = Files(
        message_id=message_id,
        file=file,
        content_type=content_type,
        is_main=is_main
    )
    return await result.create()


async def get_file(id):
    query = db.text('''
        SELECT * FROM files
        WHERE id=:id
    ''')
    return await db.first(query, id=id)


async def get_message_files(message_id):
    query = db.text('''
        SELECT * FROM files
        WHERE message_id=:message_id
    ''')
    return await db.all(query, message_id=message_id)


# Users


async def check_user(login):
    try:
        user = await Users.query.where(Users.login == login).gino.first()
    except:
        user = None
    return user


async def create_user(
        login,
        name,
        lastName,
        number,
        email,
        password,
        description,
        file_id
):
    result = Users(
        login=login,
        name=name,
        lastName=lastName,
        number=number,
        email=email,
        password=password,
        description=description,
        file_id=file_id
    )
    return await result.create()


async def create_user_chat(chat_id, user_id):
    result = UsersChats(
        chat_id=chat_id,
        user_id=user_id,
        needToAnswer=False
    )
    return await result.create()


async def get_user_chats(user_id):
    query = db.text('''
        SELECT
            "usersChats".*,
            chats.title,
            chats.description,
            chats.created_date,
            chats.status
        FROM "usersChats"
        INNER JOIN chats
        ON chat_id=chats.id
        WHERE user_id=:user_id
        ORDER BY created_date
        DESC
    ''')
    return await db.all(query, user_id=user_id)


async def get_user(login):
    query = db.text('''
       SELECT * FROM users
        WHERE login=:login
    ''')
    return await db.first(query, login=login)


# Messangers


async def create_message(
        chat_id,
        user_id,
        text,
        reply_message_id,
        type
):
    result = Messages(
        chat_id=chat_id,
        user_id=user_id,
        created_date=datetime.today(),
        text=text,
        reply_message_id=reply_message_id,
        type=type
    )
    return await result.create()


async def get_chats_messages(chat_id):
    query = db.text('''
        SELECT
            messages.id,
            users.id,
            users.name,
            users."lastName",
            users.file_id,
            messages.text,
            messages.created_date,
            messages.type,
            reply_message.id as reply_id,
            reply_message.text as reply_text
        FROM messages
        LEFT JOIN messages as reply_message
        ON messages.reply_message_id=reply_message.id
        LEFT JOIN users
        ON messages.user_id=users.id
        WHERE messages.chat_id=:chat_id
        ORDER BY messages.created_date
    ''')
    return await db.all(query, chat_id=chat_id)


async def get_message(message_id):
    query = db.text('''
        SELECT
            messages.id,
            users.id,
            users.name,
            users."lastName",
            users.file_id,
            messages.text,
            messages.created_date,
            messages.type,
            reply_message.id as reply_id,
            reply_message.text as reply_text
        FROM messages
        LEFT JOIN messages as reply_message
        ON messages.reply_message_id=reply_message.id
        LEFT JOIN users
        ON messages.user_id=users.id
        WHERE messages.id=:message_id
    ''')
    return await db.all(query, message_id=message_id)
