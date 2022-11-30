from uuid import UUID

from sanic.request import Request

from model.transaction_model import TransactionModel
from model.user_model import UserModel
from model.distribution_model import DistributionModel
from utils.validator import Validator
from sanic.response import json as json_response


class UserController:

    @staticmethod
    async def get_all_transactions(request: Request):
        user_id = request['session']['id']
        transactions = await TransactionModel().get_all_transactions(user_id) or []
        return json_response(transactions)

    @staticmethod
    async def get_all_users(request: Request):
        users = await UserModel().get_all_users()
        return json_response(users)

    @staticmethod
    async def get_user_transaction(request: Request, user_id: UUID):
        transactions = await TransactionModel().get_transaction_by_user_id(str(user_id))
        return json_response(transactions)

    @staticmethod
    async def get_user_profile(request: Request):

        user = request['session']['username']
        user = await UserModel().find_by_username(user)
        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'user not found'}, status=404)

        return json_response(user[0])

    @staticmethod
    async def set_user_sure_name(request: Request):

        body = request.json
        validator = Validator(['name'], {'name': {'type': 'str', 'min': 2}})
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        user_id = request['session']['id']
        user = await UserModel().set_sure_name(body['name'], user_id)
        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'user not found'}, status=404)

        return json_response(user[0])

    @staticmethod
    async def set_user_firebase_token(request: Request):

        body = request.json
        validator = Validator(['firebase_token'], {'firebase_token': {'type': 'str'}})
        validate_response = validator.validate(body)

        if validate_response['error']:
            return json_response(validate_response, status=400)

        user_id = request['session']['id']
        user = await UserModel().set_firebase_token(body['firebase_token'], user_id)
        if user is None or len(user) == 0:
            return json_response({'error': True, 'message': 'user not found'}, status=404)

        return json_response(user[0])

    @staticmethod
    async def check_for_update(request: Request):
        body = request.json
        validator = Validator(
            ['version_code', 'keyword'],
            {'version_code': {'type': 'int'}, 'keyword': {'handler': Validator.is_uuid}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        user_keyword = body['keyword']
        app = await DistributionModel().get_latest_app(user_keyword)
        if app is None or len(app) == 0:
            return json_response({'error': False, 'message': 'no update'})

        version_code = app[0]['version_code']
        if body['version_code'] < version_code:
            return json_response(app[0])
        
        return json_response({'error': False, 'message': 'no update'})
