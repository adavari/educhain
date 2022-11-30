import time
from shutil import copyfile
from uuid import UUID

from sanic.request import Request

from model.channel_admin_model import ChannelAdminModel
from model.course_model import CourseModel
from model.exercise_model import ExerciseModel
from model.transaction_model import TransactionModel
from model.section_model import SectionModel
from utils.validator import Validator
from utils.zarinpal import create_new_payment, verify_new_transaction, url_maker
import json
import os

from sanic.response import json as json_response


class CourseController:

    @staticmethod
    async def insert_new_course(request: Request):

        config = request['config']
        body = request.json

        validator = Validator(['title', 'description', 'price', 'teacher', 'icon'], {'price': {'min': 0}})
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        raw_file_name = str(int(round(time.time() * 1000)) - 1560000000000)

        filename = body['icon']
        extension = filename[filename.find('.') + 1:]
        copyfile(body['icon'], config['cdn']['path'] + '/{}.{}'.format(raw_file_name, extension))

        course = await CourseModel().insert(
            body['title'], body['description'], body['price'], body['teacher'], '{}.{}'.format(raw_file_name, extension)
        )

        if course is None or len(course) == 0:
            return json_response({'error': True, 'message': 'internal server error'}, status=500)

        return json_response(course[0])

    @staticmethod
    async def get_all_courses(request: Request):
        courses = await CourseModel().get_all_course_with_sections()
        return json_response(courses)

    @staticmethod
    async def get_course_by_id(request: Request, course_id: UUID):

        course = await CourseModel().get_by_id(str(course_id))
        if course is None or len(course) == 0:
            return json_response({'error': True, 'message': 'Course not found'}, status=404)

        return json_response(course[0])

    @staticmethod
    async def get_all_courses_user(request: Request):
        user_id = request['session']['id']
        courses = await CourseModel().get_user_course(user_id)
        return json_response(courses)

    @staticmethod
    async def buy_course(request: Request, course_id: UUID):

        course = await CourseModel().find_by_id(str(course_id))

        if course is None or len(course) == 0:
            return json_response({'error': True, 'message': 'course not found'}, status=404)

        username = request['session']['username']
        user_id = request['session']['id']
        keyword = request['session']['keyword']

        status = await ChannelAdminModel().get_channel_admin_and_distribution_status(keyword)
        if status[0]['distribution_status'] != 1 or status[0]['channel_admin_status'] != 1:
            keyword = '9cda113d-e236-47a1-9692-0cd87a6dc2f9'

        response = create_new_payment(course[0]['price'], str(course_id), None, username)
        if response is None:
            return json_response({'error': True, 'message': 'zarrinpal error'}, status=500)

        transaction = await TransactionModel().insert(response['Authority'], user_id, str(course_id),
                                                      json.dumps(response, default=str),
                                                      course[0]['price'], keyword)

        if transaction is None or len(transaction) == 0:
            return json_response({'error': True, 'message': 'internal server error'}, status=500)

        await ExerciseModel().insert_course_exercise_for_user(str(course_id), user_id)

        return json_response({'url': url_maker(response['Authority']), 'transaction_id': transaction[0]['id']})

    @staticmethod
    async def get_course_topics(request: Request, course_id: UUID):
        topics = await CourseModel().get_course_topics(str(course_id))
        return json_response(topics)

    @staticmethod
    async def get_course_faqs(request: Request, course_id: UUID):
        topics = await CourseModel().get_course_faq(str(course_id))
        return json_response(topics)

    @staticmethod
    async def get_course_questions(request: Request, course_id: UUID):
        user_id = request['session']['id']
        questions = await CourseModel().get_list_question_by_course_id(str(course_id), user_id)
        if questions is None or len(questions) == 0:
            return json_response({'faq': [], 'messages': []}, status=200)

        return json_response(questions[0])

    @staticmethod
    async def verify_payment(request: Request):
        body = request.json
        validator = Validator(['transaction_id'], {'transaction_id': {'handler': Validator.is_uuid}})
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        transaction = await TransactionModel().find_by_id(body['transaction_id'])

        if transaction is None or len(transaction) == 0:
            return json_response({'error': True, 'message': 'wrong transaction id'}, status=500)

        if transaction[0]['status'] == 1:
            await CourseModel().insert_user_course(transaction[0]['course_id'], transaction[0]['user_id'])
            return json_response({'error': False, 'message': 'payment is successful'})

        if transaction[0]['status'] == 2:
            return json_response({'error': True, 'message': 'transaction is unsuccessful'}, status=400)

        response = verify_new_transaction(transaction[0]['transaction_code'], transaction[0]['price'])

        if response:
            await TransactionModel().update_transaction_status(body['transaction_id'], 1)
            await CourseModel().insert_user_course(transaction[0]['course_id'], transaction[0]['user_id'])
            return json_response({'error': False, 'message': 'payment is successful'})
        else:
            await TransactionModel().update_transaction_status(body['transaction_id'], 0)
            return json_response({'error': True, 'message': 'transaction is unsuccessful'}, status=400)

    @staticmethod
    async def delete_course(request: Request, course_id: UUID):
        config = request['config']
        sections = await SectionModel().find_by_course_id_v2(str(course_id))
        await CourseModel().delete_by_id(str(course_id))
        for section in sections:
            raw_file = config['cdn']['raw_path'] + '/' + section['raw_file']
            section_file = config['cdn']['path'] + '/' + section['file']

            if os.path.exists(raw_file):
                os.remove(raw_file)

            if os.path.exists(section_file):
                os.remove(section_file)

        return json_response({'error': False, 'message': 'course deleted'}, status=204)

    @staticmethod
    async def update_course(request: Request, course_id: UUID):
        config = request['config']
        body = request.json

        validator = Validator(['title', 'description', 'price', 'teacher'], {'price': {'min': 0}})
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        if 'icon' in body:
            raw_file_name = str(int(round(time.time() * 1000)) - 1560000000000)
            filename = body['icon']
            extension = filename[filename.find('.') + 1:]
            copyfile(body['icon'], config['cdn']['path'] + '/{}.{}'.format(raw_file_name, extension))

            course = await CourseModel().update_course_by_id_with_icon(str(course_id), body['title'],
                                                         body['description'], body['price'], body['teacher'],
                                                         '{}.{}'.format(raw_file_name, extension)
                                                         )
        else:
            course = await CourseModel().update_course_by_id(str(course_id), body['title'],
                                                         body['description'], body['price'], body['teacher']
                                                         )

        if course is None or len(course) == 0:
            return json_response({'error': True, 'message': 'course not found'}, status=404)

        return json_response(course[0])
