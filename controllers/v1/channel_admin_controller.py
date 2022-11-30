import datetime
from uuid import UUID

from sanic.request import Request

from model.channel_admin_model import ChannelAdminModel
from model.distribution_model import DistributionModel
from model.transaction_model import TransactionModel
from utils.jwt import generate_jwt_token
from utils.utils import random_string
from utils.validator import Validator
from sanic.response import json as json_response


class ChannelAdminController:

    @staticmethod
    async def create_new_admin(request: Request):

        body = request.json
        validator = Validator(
            ['username', 'password', 'name'],
            {'username': {'min': 3, 'type': 'str'}, 'password': {'min': 6, 'type': 'str'},
             'name': {'min': 2, 'type': 'str'}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        is_exists = await ChannelAdminModel().find_by_username(body['username'])

        if is_exists is not None and len(is_exists) > 0:
            return json_response({'error': True, 'message': 'username already exists'}, status=401)

        admin = await ChannelAdminModel().insert(body['username'], body['password'], body['name'])

        if admin is None or len(admin) == 0:
            return json_response({'error': True, 'message': 'internal server error'}, status=500)

        return json_response({'error': False, 'message': 'channel admin created successfully'})

    @staticmethod
    async def login(request: Request):

        body = request.json
        validator = Validator(
            ['username', 'password'],
            {'username': {'min': 3, 'type': 'str'}, 'password': {'min': 6, 'type': 'str'}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        admin = await ChannelAdminModel().get_by_username_and_password(body['username'], body['password'])

        if admin is None or len(admin) == 0:
            return json_response({'error': True, 'message': 'username or password is wrong'}, status=401)

        token = generate_jwt_token(admin[0])
        return json_response({"error": False, "token": token})

    @staticmethod
    async def update_channel_account(request: Request):
        body = request.json

        admin = request['session']

        # validate_response = validate(body, ['name'])
        # if validate_response['error']:
        #     return json_response(validate_response, status=400)

        payment_account = None
        payment_bank_name = None
        credit_card_number = None
        credit_card_name = None

        if 'payment_account' in body:
            payment_account = body['payment_account']
            if 'payment_bank_name' in body:
                payment_bank_name = body['payment_bank_name']
            else:
                return json_response({'error': True,
                                      'message': 'If you send the <payment_account>, you must also send <payment_bank_name>'},
                                     status=400)

        if 'credit_card_number' in body:
            credit_card_number = body['credit_card_number']
            if 'credit_card_name' in body:
                credit_card_name = body['credit_card_name']
            else:
                return json_response({'error': True,
                                      'message': 'If you send the <credit_card_number>, you must also send <credit_card_name>'},
                                     status=400)

        if payment_account is None and credit_card_number is None:
            return json_response({'error': True,
                                  'message': 'You must submit one of the credit_card_number or payment_account'},
                                 status=400)

        admin = await ChannelAdminModel().update_data(admin['id'], payment_account, payment_bank_name,
                                                      credit_card_number,
                                                      credit_card_name)
        if admin is None or len(admin) == 0:
            return json_response({'error': True, 'message': 'admin not found'}, status=404)

        return json_response({'error': False, 'message': 'channel admin updated successfully'})

    @staticmethod
    async def set_channel_admin_status(request: Request, channel_admin_id: UUID):
        body = request.json
        validator = Validator(
            ['status']
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        admin = await ChannelAdminModel().update_status(str(channel_admin_id), body['status'])
        if admin is None or len(admin) == 0:
            return json_response({'error': True, 'message': 'admin not found'}, status=404)

        if body['status'] == 2 or body['status'] == '2':
            await ChannelAdminModel().disable_all_channel_admin_distributions(str(channel_admin_id))

        return json_response({'error': False, 'message': 'channel admin status updated successfully'})

    @staticmethod
    async def add_channel(request: Request):
        body = request.json
        admin = request['session']
        validator = Validator(
            ['name', 'platform', 'channel_id'],
            {'name': {'min': 3, 'type': 'str'}, 'platform': {'min': 2, 'type': 'str'},
             'channel_id': {'handler': Validator.is_uuid}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        is_exists = await DistributionModel().find_by_platform_and_channel_id(body['platform'], body['channel_id'])
        if is_exists is not None and len(is_exists) > 0:
            return json_response({'error': True, 'message': 'channel exists'}, status=401)

        dist = await DistributionModel().insert(body['name'], body['platform'], body['channel_id'], admin['id'])
        if dist is None or len(dist) == 0:
            return json_response({'error': True, 'message': 'internal server error'}, status=500)

        return json_response({'error': False, 'message': 'channel admin created successfully'})

    @staticmethod
    async def get_channel_by_owner(request: Request):
        admin = request['session']
        channels = await DistributionModel().get_by_owner(admin['id'])
        return json_response(channels)

    @staticmethod
    async def get_all_channel_admins(request: Request):
        channel_admins = await ChannelAdminModel().get_channel_admin_with_channels()
        return json_response(channel_admins, status=200)

    @staticmethod
    async def get_channel_admin_transactions(request: Request):
        admin_id = request['session']['id']
        transactions = await ChannelAdminModel().get_channel_success_transactions(admin_id)
        return json_response(transactions)

    @staticmethod
    async def update_distribution_status(request: Request, distribution_id: UUID):
        body = request.json

        validator = Validator(
            ['status']
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        if body['status'] == 1 or  body['status'] == '1':
            status = await ChannelAdminModel().get_channel_admin_and_distribution_status(str(distribution_id))
            if status is None or len(status) == 0:
                return json_response({'error': True, 'message': 'disribution not found'}, status=404)
            status = status[0]
            if status['channel_admin_status'] != 1:
                return json_response({'error': True, 'message': 'channel_admin not confirmed'}, status=400)

        disribution = await DistributionModel().update_status(str(distribution_id), body['status'])
        if disribution is None or len(disribution) == 0:
            return json_response({'error': True, 'message': 'disribution not found'}, status=404)

        if body['status'] == 1 or body['status'] == '1':
            await DistributionModel().insert_dist_by_dist_id(str(distribution_id))

        return json_response({'error': False, 'message': 'disribution status updated successfully'})

    @staticmethod
    async def get_channel_admin_profile(request: Request):
        admin_id = request['session']['id']
        profile = await ChannelAdminModel().get_channel_admin_profile(admin_id)
        if profile is None or len(profile) == 0:
            return json_response({'error': True, 'message': "can't find profile"}, status=500)

        return json_response(profile[0])

    @staticmethod
    async def get_distribution_app(request: Request):
        admin_id = request['session']['id']
        apps = await ChannelAdminModel().get_distribution_app(admin_id)
        return json_response(apps)

    @staticmethod
    async def get_balances(request: Request):
        admin_id = request['session']['id']
        balances = await ChannelAdminModel().get_channel_admin_balances(admin_id)
        if balances is None or len(balances) == 0:
            return json_response({'error': True, 'message': "can't find channeladmin"}, status=500)

        return json_response(balances)

    @staticmethod
    async def get_channel_admin_distribution(request: Request, channel_admin_id: UUID):
        distributions = await DistributionModel().get_by_channel_admin_id(str(channel_admin_id))
        if distributions is None or len(distributions) == 0:
            return json_response({'error': True, 'message': 'channel_admin not found'}, status=404)

        return json_response(distributions[0])

    @staticmethod
    async def get_distribution_transactions(request: Request, distribution_id: UUID):
        distributions = await TransactionModel().get_by_distribution_id(str(distribution_id))
        if distributions is None or len(distributions) == 0:
            json_response({'error': True, 'message': 'distribution not found'}, status=404)

        return json_response(distributions[0])

    @staticmethod
    async def get_recoupment_account(request: Request, channel_admin_id: UUID):

        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        if 'to' in request.args:
            to = request.args['to'][0]
        else:
            to = tomorrow

        if 'from' in request.args:
            from_date = request.args['from'][0]
        else:
            from_date = '1970-01-01'

        recoupment = await ChannelAdminModel().get_recoupment_account(str(channel_admin_id), from_date, to)
        return json_response(recoupment)

    @staticmethod
    async def admin_reset_password(request: Request, channel_admin_id: UUID):
        random_password = random_string(8)
        channel_admin = await ChannelAdminModel().change_password(channel_admin_id=str(channel_admin_id),
                                                                  password=random_password)
        if channel_admin is None or len(channel_admin) is 0:
            return json_response({'error': True, 'message': 'channel_admin not found'}, status=404)
        return json_response({'new_password': random_password})

    @staticmethod
    async def channel_admin_reset_password(request: Request):
        body = request.json
        validator = Validator(
            ['old_password', 'new_password'],
            {'old_password': {'min': 6, 'type': 'str'}, 'new_password': {'min': 6, 'type': 'str'}}
        )
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        admin_id = request['session']['id']

        channel_admin = await ChannelAdminModel().find_by_id_and_password(admin_id, body['old_password'])
        if channel_admin is None or len(channel_admin) == 0:
            return json_response({'error': True, 'message': 'wrong password'}, status=401)

        await ChannelAdminModel().change_password(admin_id, body['new_password'])
        return json_response({'error': False, 'message': 'password changed successful'})
