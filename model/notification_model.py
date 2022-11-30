from .base_model import BaseModel


class NotificationModel(BaseModel):

    def __init__(self):
        super().__init__('public.notification', 'aa974a97-82dd-4c25-a4d0-aa6a420c3a6e')

    async def insert_public(self, title: str, body: str):
        query = """
            insert into public.notification (title, body)
            values(%s, %s)
            returning *;
        """

        return await self.run_query(query, [title, body])

    async def insert_single(self, title: str, body: str, firebase_token: str):
        query = """
            insert into public.notification (title, body, push_type, firebase_token)
            values(%s, %s, 2, %s)
            returning *;
        """

        return await self.run_query(query, [title, body, firebase_token])

    def find_not_send_sync(self):
        query = """
            select * from public.notification
            where status=0
        """

        return self.run_query_sync(query)

    def update_notification_sync(self, notification_id: str, status: int, result: str):
        query = """
            update notification
            set status=%s, result_log=%s
            where id=%s
            returning *;
        """

        return self.run_query_sync(query, [status, result, notification_id])


