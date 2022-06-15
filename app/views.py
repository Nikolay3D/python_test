import aiohttp_jinja2
import os
import json
import syslog
from aiohttp import web

used_daemon = "wpa_supplicant"
app_states_filepath = 'states.json'


# TODO
# - Можно ли сделать редирект на '/' не прописывая функцию в каждом роуте?
# - При выполнении редиректа информация о сервисе может не успеть обновиться.
#   - Сделать периодическое обновление страницы на клиенте?
#   - Дождаться пока команда управления сервисом точно отработает и потом делать редирект? - клиент не поймет почему висим
# - Шаблон заполняется на стороне сервера. Может передать JSON на клиент, а там пусть рулит к.н. React..
# - Красиво оформить страничку
# ******************************************************************************************
# - поискать еще примеры готовых решений
# - добавить БД
# - Дополнить до REST


def init_base():
    app_states = {
        'control': False,
    }
    try:
        with open(app_states_filepath, 'w') as outfile:
            outfile.write(json.dumps(app_states))
        syslog.syslog("base init")
    except:
        syslog.syslog(syslog.LOG_ERR, "base init fail")


def get_control_state():
    state = False
    try:
        with open(app_states_filepath) as json_file:
            app_states = json.load(json_file)
            if "control" in app_states:
                state = app_states["control"]
    except:
        syslog.syslog(syslog.LOG_ERR, "get_control_state fail")
    finally:
        return state

def toggle_control_state():
    try:
        with open(app_states_filepath) as json_file:
            states = json.load(json_file)
            json_file.close()

            if "control" in states:
                states["control"] = not states["control"]
                with open(app_states_filepath, 'w') as outfile:
                    outfile.write(json.dumps(states))
    except:
        syslog.syslog(syslog.LOG_ERR, "toggle_control_state fail")
    finally:
        syslog.syslog(f"toggle_control_state={states['control']}")


def data_index():
    if not os.path.exists(app_states_filepath):
        init_base()

    state = os.popen("systemctl status wpa_supplicant.service | awk '/Active/ {print $2 $3}'").read()
    control_state = get_control_state()
    return {"daemon_name": f"{used_daemon}",
            "daemon_state": f"{state}",
            "btn_control_text": f"{'Disable control' if control_state else 'Enable control'}",
            "btn_start_state": f"{'' if control_state else 'disabled'}",
            "btn_restart_state": f"{'' if control_state else 'disabled'}",
            "btn_stop_state": f"{'' if control_state else 'disabled'}",
            }


@aiohttp_jinja2.template("index.html")
async def index(request):
    syslog.syslog(f"{request}")
    return data_index()


@aiohttp_jinja2.template("index.html")
async def stop(request):
    syslog.syslog(f"{request}")
    os.popen("systemctl stop wpa_supplicant.service")
    raise web.HTTPFound("/")


@aiohttp_jinja2.template("index.html")
async def start(request):
    syslog.syslog(f"{request}")
    os.popen("systemctl start wpa_supplicant.service")
    raise web.HTTPFound("/")


@aiohttp_jinja2.template("index.html")
async def restart(request):
    syslog.syslog(f"{request}")
    os.popen("systemctl restart wpa_supplicant.service")
    raise web.HTTPFound("/")


@aiohttp_jinja2.template("index.html")
async def toggle_control(request):
    syslog.syslog(f"{request}")
    toggle_control_state()
    raise web.HTTPFound("/")
