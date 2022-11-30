from uuid import UUID

from sanic.request import Request
from sanic.response import json as json_response

from model.message_model import MessageModel
from model.notification_model import NotificationModel
from model.user_model import UserModel
from utils.validator import Validator


class MessageController:

    @staticmethod
    async def get_all_messages(request: Request):
        user_id = request['session']['id']
        messages = await MessageModel().get_all_messages_by_user_id(user_id) or []

        return json_response(messages)

    @staticmethod
    async def get_all_messages_admin(request: Request):
        messages = await MessageModel().get_all_messages()
        return json_response(messages)

    @staticmethod
    async def send_message(request: Request):
        user_id = request['session']['id']
        body = request.json

        validator = Validator(
            ['title', 'message', 'course_id'],
            {'title': {'min': 2, 'max': 256, 'type': 'str'}, 'message': {'type': 'str', 'max': 501},
             'course_id': {'handler': Validator.is_uuid}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        message = await MessageModel().insert(user_id, body['title'], body['message'], body['course_id'])
        if message is None or len(message) == 0:
            return json_response({'error': True, 'message': 'please insert title and message correctly'},
                                status=400)

        message = message[0]

        return json_response(message)

    @staticmethod
    async def delete_message(request: Request, message_id: UUID):
        await MessageModel().delete_by_id(str(message_id))
        return json_response({}, status=204)

    @staticmethod
    async def get_message_by_id(request: Request, message_id: UUID):
        message = await MessageModel().find_by_id(str(message_id))
        if message is None or len(message) == 0:
            return json_response({'error': True, 'message': 'message not found'}, status=404)
        return json_response(message[0])

    @staticmethod
    async def response_message(request: Request, message_id: UUID):

        body = request.json

        validator = Validator(
            ['response'],
            {'title': {'max': 501, 'type': 'str'}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        message = await MessageModel().response_to_message(str(message_id), body['response'])
        if message is None or len(message) == 0:
            return json_response({'error': True, 'message': 'message not found'}, status=404)

        message = await MessageModel().find_by_id(str(message_id))
        user_id = message[0]['user_id']

        user = await UserModel().find_by_id(user_id)
        firebase_token = user[0]['firebase_token']

        await NotificationModel().insert_single(' ', 'به پیام شما توسط مدیر پاسخ داده شد', firebase_token)

        return json_response(message[0])
