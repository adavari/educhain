from .base_model import BaseModel
from uuid import uuid5

import hashlib

class AdminUser(BaseModel):

    def __init__(self):
        super().__init__('public.admin_user', '33662fee-c458-409e-bffd-be72e3463db4')

    async def insert(self, username: str, password: str):
        query = """
            insert into public.admin_user (id, username, password)
            values (%s, %s, %s)
            on conflict (id) do update set updated_at=now()
            returning *;
        """

        id = str(uuid5(self.namespace, username))
        password = hashlib.sha1(password.encode()).hexdigest()

        return await self.run_query(query, [id, username, password])

    async def login(self, username: str, password: str):
        query = """
            update public.admin_user
            set last_login=now(), updated_at=now()
            where username=%s and password=%s
            returning *;
        """

        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [username, password])
