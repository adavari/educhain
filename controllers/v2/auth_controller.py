from sanic.request import Request
from sanic.response import json as json_response

from model.user_model import UserModel
from utils.encryptor import create_reset_password_token, validate_password_reset_token
from utils.jwt import generate_jwt_token
from utils.validator import Validator


class AuthController:

    @staticmethod
    async def signup(request: Request):
        body = request.json

        validator = Validator(
            ['username', 'password', 'surename', 'keyword'],
            {'username': {'type': 'str', 'min': 3}, 'password': {'type': 'str', 'min': 6},
             'keyword': {'handler': Validator.is_uuid}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, ccccc=400)
        ref_code = '0'

        is_exists = await UserModel().find_by_username(body['username'])

        if is_exists is not None and len(is_exists) > 0:
            return json_response({'error': True, 'message': 'username already exists'}, status=400)

        user = await UserModel().insert_v2(body['username'], body['password'], ref_code, body['surename'],
                                           body['keyword'])

        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'something wrong :)'}, status=500)

        await UserModel().enable_user(body['username'])
        return json_response({'error': False, 'message': 'user created'})

    @staticmethod
    async def login(request: Request):

        body = request.json

        validator = Validator(
            ['username', 'password', 'keyword'],
            {'username': {'type': 'str', 'min': 3}, 'password': {'type': 'str', 'min': 6}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        user = await UserModel().find_by_username_and_password_and_keyword(body['username'], body['password'], body['keyword'])

        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'username or password is wrong!'}, status=401)

        token = generate_jwt_token(user[0])
        return json_response({"error": False, "token": token})

    @staticmethod
    async def update_password_request(request: Request):
        
        body = request.json
        validator = Validator(
            ['username', 'password', 'keyword'],
            {'username': {'type': 'str', 'min': 3}, 'password': {'type': 'str', 'min': 6}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        user = await UserModel().find_by_username_and_password(body['username'], body['password'])
        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'username or password is wrong!'}, status=400)

        response = create_reset_password_token(user[0]['id'])
        return json_response(response)

    @staticmethod
    async def update_password(request: Request):
        body = request.json
        validator = Validator(
            ['username', 'password', 'keyword', 'token', 'code', 'new_password'],
            {'username': {'type': 'str', 'min': 3}, 'password': {'type': 'str', 'min': 6},
             'new_password': {'type': 'str', 'min': 6}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        user = await UserModel().find_by_username_and_password(body['username'], body['password'])
        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'username is wrong!'}, status=401)

        response = validate_password_reset_token(user[0]['id'], body['code'], body['token'])
        if response:
            user = await UserModel().update_password(body['username'], body['new_password'])
            if user is None or len(user) == 0:
                return json_response({'error': True, 'message': 'username is wrong!'}, status=400)
            return json_response({'error': False, 'message': 'password changed'})

        else:
            return json_response({'error': True, 'message': 'invalid token or code!'}, status=400)

