from sanic.request import Request

from model.admin_user_model import AdminUser
from model.distribution_model import DistributionModel
from utils.jwt import generate_jwt_token
from utils.validator import Validator
from sanic.response import json as json_response


class AdminController:

    @staticmethod
    async def created_user(request: Request):

        body = request.json
        validator = Validator(
            ['username', 'password'],
            {'username': {'min': 3}, 'password': {'min': 8}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        admin_user = await AdminUser().insert(body['username'], body['password'])

        if admin_user is None or len(admin_user) == 0:
            return json_response({'error': True, 'message': 'internal server error'}, status=500)

        return json_response({'error': False, 'message': 'user created successfully'})

    @staticmethod
    async def login(request: Request):

        body = request.json

        validator = Validator(
            ['username', 'password'],
            {'username': {'min': 3}, 'password': {'min': 8}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        admin_user = await AdminUser().login(body['username'], body['password'])

        if admin_user is None or len(admin_user) == 0:
            return json_response({'error': True, 'message': 'username or password is wrong'}, status=400)

        token = generate_jwt_token(admin_user[0])
        return json_response({"error": False, "token": token})

    @staticmethod
    async def add_new_app_version(request: Request):
        body = request.json
        validator = Validator(
            ['version_code'],
            {'version_code': {'type': 'int'}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        apps = await DistributionModel().insert_new_app_version(body['version_code'])
        if apps is None or len(apps) == 0:
            return json_response({'error': True, 'message': 'oops someting get wrong :)'}, status=400)

        dists = await DistributionModel().insert_dist_apps()
        if dists is None or len(dists) == 0:
            return json_response({'error': True, 'message': 'oops someting get wrong :)'}, status=400)

        return json_response({"error": False, "message": "new version added start building :)"})
