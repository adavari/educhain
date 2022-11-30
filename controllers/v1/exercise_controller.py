import json as Json
from uuid import UUID

from sanic.request import Request

from model.exercise_model import ExerciseModel
from utils.validator import Validator
from sanic.response import json as json_response


class ExerciseController:

    @staticmethod
    async def get_all(request: Request):
        exercise = await ExerciseModel().find_all()
        data = Json.loads(Json.dumps(exercise, default=str))
        return json_response(data)

    @staticmethod
    async def add_exercise(request: Request):
        body = request.json

        validator = Validator(
            ['title', 'description', 'receive_day', 'receive_time',  'section_id'],
            {'section_id': {'handler': Validator.is_uuid}}
        )
        validate_response = validator.validate(body)

        if validate_response['error']:
            return json_response(validate_response, status=400)

        exercise = await ExerciseModel().insert(body['title'], body['description'], body['receive_day'],
                                                body['receive_time'], body['section_id'])

        if exercise is None or len(exercise) == 0:
            return json_response({'error': True, 'message': 'internal error'}, status=500)

        data = Json.loads(Json.dumps(exercise[0], default=str))
        return json_response(data)

    @staticmethod
    async def get_by_course(request: Request, course_id: UUID):
        course = await ExerciseModel().get_by_course_id(str(course_id))
        data = Json.loads(Json.dumps(course, default=str))
        return json_response(data)

    @staticmethod
    async def get_by_section(request: Request, section_id: UUID):
        section = await ExerciseModel().get_by_section_id(str(section_id))
        data = Json.loads(Json.dumps(section, default=str))
        return json_response(data)

    @staticmethod
    async def get_user_exercise(request: Request):
        user_id = request['session']['id']
        exercise = await ExerciseModel().get_user_exercise(user_id)

        data = Json.loads(Json.dumps(exercise, default=str))
        return json_response(data)

    @staticmethod
    async def add_user_exercise(request: Request):
        user_id = request['session']['id']
        body = request.json

        validator = Validator(
            ['title', 'description', 'receive_day', 'receive_time', 'section_id'],
            {'section_id': {'handler': Validator.is_uuid}}
        )

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        exercise = await ExerciseModel().insert(body['title'], body['description'], body['receive_day'],
                                                body['receive_time'], body['section_id'])

        if exercise is None or len(exercise) == 0:
            return json_response({'error': True, 'message': 'internal error'}, status=500)

        course_id = exercise[0]['course_id']

        await ExerciseModel().insert_course_exercise_for_user(course_id, user_id)

        data = Json.loads(Json.dumps(exercise[0], default=str))
        return json_response(data)

    @staticmethod
    async def add_response(request: Request, exercise_id: UUID):
        user_id = request['session']['id']
        body = request.json

        validator = Validator(['response'])

        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        exercise = await ExerciseModel().add_response(body['response'], str(exercise_id), user_id)

        if exercise is None or len(exercise) == 0:
            return json_response({'error': True, 'message': 'exercise nit found'}, status=404)

        data = Json.loads(Json.dumps(exercise[0], default=str))
        return json_response(data)

    @staticmethod
    async def delete_exercise(request: Request, exercise_id: UUID):
        await ExerciseModel().delete_by_id(str(exercise_id))
        return json_response({}, status=204)

    @staticmethod
    async def update_exercise(request: Request, exercise_id: UUID):
        body = request.json

        validator = Validator(['title', 'description', 'receive_day', 'receive_time'])
        validate_response = validator.validate(body)
        if validate_response['error']:
            return json_response(validate_response, status=400)

        exercise = await ExerciseModel().update(str(exercise_id), body['title'], body['description'],
                                                body['receive_day'], body['receive_time'])
        if exercise is None or len(exercise) == 0:
            return json_response({'error': True, 'message': 'exercise not found'}, status=404)
        
        data = Json.loads(Json.dumps(exercise[0], default=str))
        return json_response(data)