from sanic.request import Request
from sanic.response import json as json_response

from model.analytics_model import AnalyticsModel
from utils.validator import Validator


class AnalyticsController:

    @staticmethod
    async def add_install(request: Request):
        body = request.json

        validator = Validator(
            ['keyword'],
            {'keyword': {'handler': Validator.is_uuid}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        await AnalyticsModel().insert(body['keyword'])

        return json_response({'error': False, 'message': 'install inserted!'})
