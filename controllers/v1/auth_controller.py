from sanic.request import Request

from model.user_model import UserModel
from utils.jwt import generate_jwt_token, decode_jwt_token
from utils.number_utils import random_digit
from utils.sms_sender import send_smd
from utils.validator import Validator
from sanic.response import json as json_response


class AuthController:

    @staticmethod
    async def otp(request: Request):
        body = request.json
        validator = Validator(
            ['username', 'keyword'],
            {'username': {'handler': Validator.is_mobile_number}, 'keyword': {'handler': Validator.is_uuid}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)
        ref_code = random_digit()
        password = '123456'
        user = await UserModel().insert(body['username'], password, ref_code, body['keyword'])

        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'something wrong :)'}, status=500)

        send_smd('کد فعال سازی شما {}'.format(ref_code), body['username'])

        return json_response({'error': False, 'message': 'otp message sent'})

    @staticmethod
    async def confirm(request: Request):

        body = request.json
        validator = Validator(
            ['username', 'code'],
            {'username': {'handler': Validator.is_mobile_number}, 'code': {'min': 4}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        user = await UserModel().find_by_username_and_ref_code(body['username'], body['code'])

        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'username or code is wrong!'}, status=404)

        token = generate_jwt_token(user[0])
        return json_response({"error": False, "token": token})

    @staticmethod
    async def refresh_token(request: Request):
        headers = request.headers

        if 'authorization' not in headers:
            return json_response({"error": True, "message": "Authentication credentials were not provided"}, status=401)

        token = headers['authorization'][7:]

        user_id = decode_jwt_token(token)['session']['id']

        user = await UserModel().find_by_id(user_id)

        if user is None or len(user) == 0:
            return json_response({"error": True, "message": "Authentication credentials were not provided"}, status=401)

        token = generate_jwt_token(user[0])
        return json_response({"error": False, "token": token})

    @staticmethod
    async def unsubscribe(request: Request):
        username = request['session']['username']

        user = await UserModel().disable_user(username)

        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'unknown error'}, status=500)

        return json_response({"error": False, "message": "user disabled successfully"})
