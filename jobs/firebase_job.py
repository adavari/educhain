# Send notifications to users through firebase

import json
import sys
import os
from model.notification_model import NotificationModel
import time
from pyfcm import FCMNotification
import logging

from model.user_model import UserModel

API_KEY = os.getenv("FIREBASE-API-KEY")
push_service = FCMNotification(api_key=API_KEY)

logger = logging.getLogger("NOTIFICATION_LOGGER")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


while True:
    time.sleep(30)
    notifications = NotificationModel().find_not_send_sync()
    for notification in notifications:

        if notification['push_type'] == 1:
            # is Public push
            f_tokens = UserModel().get_firebase_tokens_sync()
            firebase_tokens = []
            for f in f_tokens:
                firebase_tokens.append(f['firebase_token'])
            message_title = notification['title']
            message_body = notification['body']

            result = push_service.notify_multiple_devices(registration_ids=firebase_tokens, message_title=message_title,
                                                          message_body=message_body)

        else:
            # is single push
            registration_id = notification['firebase_token']
            message_title = notification['title']
            message_body = notification['body']

            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)

        json_result = json.dumps(result)
        NotificationModel().update_notification_sync(notification_id=notification['id'], status=1, result=json_result)
        logger.info("notification with id {} is sent".format(notification['id']))


