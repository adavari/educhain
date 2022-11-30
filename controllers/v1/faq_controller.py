from uuid import UUID

from sanic.request import Request

from model.faq_model import FaqModel
from utils.validator import Validator
from sanic.response import json as json_response


class FaqController:

    @staticmethod
    async def get_all_faqs(request: Request):

        faqs = await FaqModel().get_all_with_course() or []

        return json_response(faqs)

    @staticmethod
    async def get_all_faqs_user(request: Request):
        faqs = await FaqModel().get_all_public_faqs() or []

        return json_response(faqs)

    @staticmethod
    async def create_new_faq(request: Request):

        body = request.json
        validator = Validator(['question', 'answer'])
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        if 'course_id' in body:
            faq = await FaqModel().insert_with_course_id(body['question'], body['answer'], body['course_id'])
        else:
            faq = await FaqModel().insert(body['question'], body['answer'])

        if faq is None or len(faq) == 0:
            return json_response({'error': True, 'message': 'internal server error'}, status=500)

        return json_response(faq[0])

    @staticmethod
    async def delete_faq(request: Request, faq_id: UUID):
        await FaqModel().delete_by_id(str(faq_id))
        return json_response({}, status=204)

    @staticmethod
    async def update_faq(request: Request, faq_id: UUID):
        body = request.json
        validator = Validator(['question', 'answer'])
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        if 'course_id' in body:
            faq = await FaqModel().update_by_id_with_course_id(str(faq_id), body['question'], body['answer'],
                                                               body['course_id'])
        else:
            faq = await FaqModel().update_by_id(str(faq_id), body['question'], body['answer'])

        if faq is None or len(faq) == 0:
            return json_response({'error': True, 'message': 'faq not found'}, status=404)

        return json_response(faq[0])
