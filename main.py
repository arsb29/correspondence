from aiohttp import web
from routes import setup_routes
from models import db
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

SECRET_KEY = "nNjpIl9Ax2LRtm-p6ryCRZ8lRsL0DtuY0f9JeAe2wG0="


async def before_server_start(app):
    await db.set_bind(app['config']['db_dsn'])
    await db.gino.create_all()


async def after_server_stop(_):
    await db.pop_bind().close()


async def create_app(config):
    app = web.Application(
        middlewares=[session_middleware(EncryptedCookieStorage(SECRET_KEY))],
        client_max_size=1024 ** 10
    )
    app['config'] = config
    setup_routes(app)
    app.on_startup.append(before_server_start)
    app.on_cleanup.append(after_server_stop)
    return app
