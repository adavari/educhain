from .base_model import BaseModel


class ExerciseModel(BaseModel):

    def __init__(self):
        super().__init__('public.exercise', '3e9fe679-f220-4922-9b12-814f6f3ec25c')

    async def insert(self, title: str, description: str, receive_day: int, receive_time: str, section_id: str):
        query = """
            insert into exercise (title, description, receive_day, receive_time, course_id, section_id)
            select %s, %s, %s, %s, course_id, %s from section
            where section.id = %s
            returning *;
        """

        return await self.run_query(query, [
            title, description, receive_day, receive_time, section_id, section_id
        ])

    async def get_by_course_id(self, course_id: str):
        query = """
            select * from public.exercise
            where course_id=%s
        """

        return await self.run_query(query, [course_id])

    async def get_by_section_id(self, section_id: str):
        query = """
            select * from public.exercise
            where section_id=%s
        """

        return await self.run_query(query, [section_id])
        
    async def insert_course_exercise_for_user(self, course_id: str, user_id: str):
        query = """
            insert into user_exercise
            select uuid_generate_v4(), id, %s, null, null from exercise
            where course_id = %s
            returning *;
        """

        return await self.run_query(query, [user_id, course_id])

    async def get_user_exercise(self, user_id: str):
        query = """
            select user_exercise.*, json_agg(exercise.*) as exercise from user_exercise
            inner join exercise on user_exercise.exercise_id = exercise.id
            where user_id = %s
            group by user_exercise.id
        """

        return await self.run_query(query, [user_id])

    async def add_response(self, response: str, exercise_id: str, user_id: str):
        query = """
            update user_exercise
            set response=%s, response_date=now(), updated_at=now()
            where exercise_id=%s and user_id=%s
            returning *;
        """

        return await self.run_query(query, [response, exercise_id, user_id])

    async def update(self, exercise_id: str, title: str, description: str, receive_day: int, receive_time: str):
        query = """
            update exercise 
            set title=%s, description=%s, receive_day=%s, receive_time=%s
            where id = %s
            returning *;
        """

        return await self.run_query(query, [
            title, description, receive_day, receive_time, exercise_id
        ])