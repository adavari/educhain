from .base_model import BaseModel


class MessageModel(BaseModel):

    def __init__(self):
        super().__init__('public.message', '807129c1-6de5-437c-af17-64435d707145')

    async def get_all_messages_by_user_id(self, user_id: str):

        query = """
            select * from public.message
            where user_id=%s
        """

        return await self.run_query(query, [user_id])

    async def insert(self, user_id: str, title: str, message: str, course_id: str):

        query = """
            insert into public.message (user_id, title, message, course_id)
            values(%s, %s, %s, %s)
            returning *;
        """
    
        return await self.run_query(query, [user_id, title, message, course_id])

    async def response_to_message(self, message_id: str, response: str):
        query = """
            update public.message
            set response=%s, updated_at=now()
            where id=%s
            returning *;
        """

        return await self.run_query(query, [response, message_id])


    async def get_all_messages(self):
        query = """
            select message.*, json_agg(users.*) as users, course.title as course_title from message
            inner join users on message.user_id = users.id
            left join course on message.course_id = course.id
            group by message.id, course.title;
        """

        return await self.run_query(query)