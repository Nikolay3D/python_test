from aiohttp import web
import jinja2
import aiohttp_jinja2
import syslog


def setup_routes(application):
    from app.routes import setup_routes as setup_app_routes
    setup_app_routes(application)


def setup_external_libraries(application: web.Application) -> None:
    # путь к шаблонам
    aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader("templates"))


def setup_app(application):
    setup_external_libraries(application)
    setup_routes(application)


if __name__ == "__main__":
    syslog.syslog('Start service control')
    app = web.Application()
    setup_app(app)
    web.run_app(app)
    syslog.closelog()
