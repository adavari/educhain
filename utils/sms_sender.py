import requests
import os

BASE_URL = "https://sms.magfa.com/magfaHttpService"
service = "Enqueue"
username = os.getenv("SMS_USERNAME")
password = os.getenv("SMS_PASSWORD")
sms_center = os.getenv("SMS_CENTER")
domain = os.getenv("SMS_DOMAIN")


def send_smd(message: str, number: str):
    response = requests.get(BASE_URL, params={
        "service": service,
        "username": username,
        "password": password,
        "from": sms_center,
        "to": number,
        "domain": domain,
        "message": message
    })

    return 200 <= response.status_code <= 299

