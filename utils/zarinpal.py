from zeep import Client
import os

MERCHANT = os.getenv("MERCHANT_ID")
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CALLBACK_URL = 'http://edu-chains.com/payment/verify/'


def create_new_payment(price: int, description: str, email: str, phone: str):
    response = client.service.PaymentRequest(MERCHANT, price, description, email, phone, CALLBACK_URL)
    if 'Authority' not in response or response['Authority'] is None:
        return None
    return response


def verify_new_transaction(authority: str, price: int):
    result = client.service.PaymentVerification(MERCHANT, authority, price)
    succes = result.Status == 100 or result.Status == 101

    return succes


def url_maker(authority: str):
    web_gate = 'https://www.zarinpal.com/pg/StartPay/{}'.format(authority)
    zarin_gate = 'https://www.zarinpal.com/pg/StartPay/{}/ZarinGate'.format(authority)
    mobile_gate = 'https://www.zarinpal.com/pg/StartPay/{}/MobileGate'.format(authority)

    return {'web_gate': web_gate, 'zarin_gate': zarin_gate, 'mobile_gate': mobile_gate}
