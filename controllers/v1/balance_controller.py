from uuid import UUID

from sanic.request import Request
from sanic.response import json as json_response
from model.balance_model import BalanceModel
from utils.validator import Validator


class BalanceController:

    @staticmethod
    async def add_balance(request: Request):
        body = request.json
        validator = Validator(
            ['channel_admin_id', 'amount'],
            {'channel_admin_id': {'handler': Validator.is_uuid}, 'amount': {'min': 1}}
        )
        validate_response = validator.validate(body, )
        if validate_response['error']:
            return json_response(validate_response, status=400)

        balance = await BalanceModel().insert(body['channel_admin_id'], body['amount'])
        if balance is None or len(balance) == 0:
            return json_response({'error': True, 'message': 'something is wrong :)'}, status=500)

        return json_response(balance[0])

    @staticmethod
    async def get_balance_by_channel_admin_id(request: Request, channel_admin_id: UUID):
        balances = await BalanceModel().find_by_channel_admin_id(str(channel_admin_id))
        if balances is None or len(balances) == 0:
            return json_response({'error': True, 'message': 'channel admin not found'}, status=404)
        return json_response(balances[0])
