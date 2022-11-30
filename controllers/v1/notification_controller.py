from uuid import UUID

from sanic.request import Request
from sanic.response import json as json_response

from model.notification_model import NotificationModel
from utils.validator import Validator


class NotificationController:

    @staticmethod
    async def add_new_notification(request: Request):
        body = request.json

        validator = Validator(
            ['title', 'body'],
            {'title': {'min': 2, 'max': 256, 'type': 'str'}, 'body': {'type': 'str', 'max': 501}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        notification = await NotificationModel().insert_public(body['title'], body['body'])
        return json_response(notification[0])

    @staticmethod
    async def get_all_notifications(request: Request):
        notification = await NotificationModel().find_all()
        return json_response(notification)


    @staticmethod
    async def get_by_id(request: Request, notification_id: UUID):
        notification = await NotificationModel().find_by_id(str(notification_id))
        if notification is None or len(notification) == 0:
            return json_response({'error': True, 'message': 'notification not found'}, status=404)

        return json_response(notification[0])
