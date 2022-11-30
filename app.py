import json
import logging
import os

import redis
from sanic import Sanic
from sanic.exceptions import NotFound, MethodNotSupported
from sanic.request import Request
from sanic.response import json as json_response

from controllers import routes
from model.error_request_model import ErrorRequestModel
from utils.jwt import decode_jwt_token, validate_token

app = Sanic()

config = {}

public_paths = []

appname = """
                      .---.     .---.
                     ( -o- )---( -o- )
                     ;-...-`   `-...-;
                    /                 \
                   /                   \
                  | /_               _\ |
                  \`'.`'"--.....--"'`.'`/
                   \  '.   `._.`   .'  /
                _.-''.  `-.,,_,,.-`  .''-._
               `--._  `'-.,_____,.-'`  _.--`
                    /                 \
                   /.-'`\   .'.   /`'-.\
                  `      '.'   '.'

"""


def read_config_file():
    global config
    global public_paths
    filename = os.getenv("KERMIT_ROOT") + '/config.json'
    with open(filename, 'r') as config_file:
        con = config_file.read()
        config = json.loads(con)
        public_paths = routes.add_routes(app)


def initialize_db():
    r = redis.Redis()
    global config
    for k in config['db'].keys():
        r.set(k, config['db'][k])


def server_error_handler(request: Request, exception: Exception):
    if request is not None:
        body = request.json
        if request.json is None:
            body = {}
        ErrorRequestModel().insert(request.path, request.method, json.dumps(body) or '{}', json.dumps(dict(request.headers)), str(exception))
    return json_response({'error': True, 'message': 'internal server error'}, status=500)


def not_found_handler(request: Request, exception: NotFound):
    return json_response({'error': True, 'message': 'url not found'}, status=404)


async def authenticate(request: Request):
    url = request.path
    headers = request.headers

    is_public = url in public_paths
    if not is_public:

        if 'authorization' not in headers:
            return json_response({"error": True, "message": "Authentication credentials were not provided"},
                                 status=403)

        is_admin = str(url).__contains__('admin')

        token = headers['authorization'][7:]

        data = decode_jwt_token(token)
        if data is None:
            return json_response({"error": True, "message": "invalid token"}, status=403)

        resp = validate_token(data)
        if resp['error']:
            return json_response(resp, status=401)

        session = data['session']

        if not is_admin:

            if session is None or len(session) == 0:
                return json_response({"error": True, "message": "user disabled"}, status=403)

            if session['status'] == 0:
                return json_response({"error": True, "message": "user disabled"}, status=403)

        request['session'] = session
        request['config'] = config

if __name__ == '__main__':
    logging.log(appname)
    read_config_file()
    initialize_db()
    app.error_handler.add(NotFound, not_found_handler)
    app.error_handler.add(MethodNotSupported, not_found_handler)
    app.error_handler.add(Exception, server_error_handler)
    app.register_middleware(authenticate, "request")
    app.run(host='127.0.0.1', port=5800, workers=10)
