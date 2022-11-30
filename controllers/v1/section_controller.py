import os
import time
from shutil import copyfile
from uuid import UUID

from sanic.request import Request
from sanic.response import json as json_response

from model.course_model import CourseModel
from model.section_model import SectionModel
from utils.validator import Validator


class SectionController:

    @staticmethod
    async def insert_new_section(request: Request):

        body = request.json
        config = request['config']

        validator = Validator(
            ['title', 'description', 'course_id', 'ordering', 'section_type', 'is_free', 'raw_file'],
            {'course_id': {'handler': Validator.is_uuid}, 'raw_file': {'handler': Validator.is_correct_path}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        raw_file_name = str(int(round(time.time() * 1000)) - 1560000000000)

        filename = body['raw_file']
        extension = filename[filename.find('.') +1:]
        copyfile(body['raw_file'], config['cdn']['raw_path'] + '/{}.{}'.format(raw_file_name, extension))
        
        raw_file = '{}.{}'.format(raw_file_name, extension)

        section = await SectionModel().insert(
            body['title'], body['description'], body['course_id'], body['ordering'], raw_file, body['section_type'], body['is_free']
        )

        if section is None or len(section) == 0:
            return json_response({'error': True, 'message': 'internal error'}, status=500)

        await CourseModel().update_status(body['course_id'], 0)

        return json_response(section[0])

    @staticmethod
    async def get_course_sections(request: Request, course_id: UUID):
        sections = await SectionModel().find_by_course_id(str(course_id)) or []
        return json_response(sections)

    @staticmethod
    async def delete_section(request: Request, section_id: UUID):
        section = await SectionModel().find_by_id(str(section_id))
        if section is None or len(section) == 0:
            return json_response({'error': True, 'message': 'section not found'}, status=404)

        config = request['config']
        await SectionModel().delete_by_id(str(section_id))

        # todo : Fix this later
        # raw_file = config['cdn']['raw_path'] + '/' + section['raw_file']
        # section_file = config['cdn']['path'] + '/' + section['file']
        #
        # if os.path.exists(raw_file):
        #     os.remove(raw_file)
        #
        # if os.path.exists(section_file):
        #     os.remove(section_file)

        return json_response({}, status=204)

    @staticmethod
    async def get_section_by_id(request: Request, section_id: UUID):
        section = await SectionModel().find_by_id(str(section_id))
        if section is None or len(section) == 0:
            return json_response({'error': True, 'message': 'section not found'}, status=404)

        return json_response(section[0])

    @staticmethod
    async def update_section(request: Request, section_id: UUID):
        body = request.json

        validator = Validator(
            ['title', 'description', 'course_id', 'ordering', 'section_type'],
            {'course_id': {'handler': Validator.is_uuid}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        section = await SectionModel().update_by_id(
            str(section_id), body['title'], body['description'], body['course_id'], body['ordering'],
            body['section_type'], body['is_free']
        )

        if section is None or len(section) == 0:
            return json_response({'error': True, 'message': 'section not found'}, status=404)
        return json_response(section[0])

