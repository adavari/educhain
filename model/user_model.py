from .base_model import BaseModel
from uuid import uuid5
import hashlib


class UserModel(BaseModel):

    def __init__(self):
        super().__init__('public.users', 'ff98fc11-eeda-4142-ab80-9395271b4cfa')

    async def insert(self, username: str, password: str, ref_code: str, keyword: str):
        try:
            query = """
                insert into public.users (id, username, password, mob_ref_code, keyword)
                values (%s, %s, %s, %s, %s)
                on conflict (id) do update set updated_at=now(), keyword=%s, mob_ref_code=%s
                returning *;
            """
            id = str(uuid5(self.namespace, username))
            password = hashlib.sha1(password.encode()).hexdigest()
            response = await self.run_query(query, [id, username, password, ref_code, keyword, keyword, ref_code])
            return response
        except Exception as e:
            return None

    async def insert_v2(self, username: str, password: str, ref_code: str, surename: str, keyword: str):
        try:
            query = """
                insert into public.users (id, username, password, mob_ref_code, sure_name, keyword)
                values (%s, %s, %s, %s, %s, %s)
                on conflict (id) do update set updated_at=now(), keyword=%s
                returning *;
            """
            id = str(uuid5(self.namespace, username))
            password = hashlib.sha1(password.encode()).hexdigest()
            response = await self.run_query(query, [id, username, password, ref_code, surename, keyword, keyword])
            return response
        except Exception as e:
            return None

    async def find_by_username_and_ref_code(self, username: str, ref_code: str):
        query = """
            update public.users
            set status=1
            where username=%s and mob_ref_code=%s
            returning *;
        """

        return await self.run_query(query, [username, ref_code])

    async def find_by_username_and_password_and_keyword(self, username: str, password: str, keyword: str):
        query = """
            update public.users
            set updated_at=now(), keyword=%s
            where username=%s and password=%s
            returning *;
        """

        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [keyword, username, password])

    async def find_by_username_and_password(self, username: str, password: str):
        query = """
            select * from public.users
            where username=%s and password=%s
        """

        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [username, password])

    async def disable_user(self, username: str):
        query = """
            update public.users
            set status = 0
            where id = %s
            returning *;
        """

        return await self.run_query(query, [str(uuid5(self.namespace, username))])

    async def enable_user(self, username: str):
        query = """
            update public.users
            set status = 1
            where id = %s
            returning *;
        """

        return await self.run_query(query, [str(uuid5(self.namespace, username))])

    async def set_profile_pic(self, username: str, profile_pic: str):
        query = """
            update public.users
            set profile_pic = %s
            where id = %s
            returning *;
        """

        return await self.run_query(query, [profile_pic, str(uuid5(self.namespace, username))])

    async def update_name(self, username: str, name: str):
        query = """
            update public.users
            set sure_name = %s
            where id = %s
            returning *;
        """
        return await self.run_query(query, [name, str(uuid5(self.namespace, username))])

    async def update_password(self, username: str, password: str):
        query = """
               update public.users
               set password = %s
               where id = %s
               returning *;
           """
        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [password, str(uuid5(self.namespace, username))])

    async def set_email(self, username: str, email: str):
        query = """
            update public.users
            set email = %s
            where id = %s
            returning *;
        """
        return await self.run_query(query, [email, str(uuid5(self.namespace, username))])

    async def find_by_username(self, username: str):
        query = """
            select username, sure_name, email, firebase_token from public.users
            where username=%s
        """

        return await self.run_query(query, [username])

    async def find_by_username_with_id(self, username: str):
        query = """
            select id, username, sure_name, email, firebase_token from public.users
            where username=%s
        """

        return await self.run_query(query, [username])

    async def set_sure_name(self, name: str, user_id: str):
        query = """
            update public.users
            set sure_name=%s
            where id=%s
            returning username, sure_name, email, firebase_token;
        """

        return await self.run_query(query, [name, user_id])

    async def set_firebase_token(self, name: str, firebase: str):
        query = """
            update public.users
            set firebase_token=%s
            where id=%s
            returning username, sure_name, email, firebase_token;
        """

        return await self.run_query(query, [name, firebase])

    async def get_all_users(self):
        query = """
            select users.id, users.username, users.sure_name, users.email, users.keyword, users.created_at, 
                users.updated_at, row_to_json(distribution.*) as distribution from users
            inner join distribution on users.keyword = distribution.id
        """
        return await self.run_query(query)

    def count_by_keyword_sync(self, dist_id: str):
        query = """
            select count(users.*) as total_users from users
            where keyword=%s and status=1
        """
        return self.run_query_sync(query, [dist_id])

    def get_firebase_tokens_sync(self):
        query = """
            select firebase_token from users
            where firebase_token is not null and status=1
        """

        return self.run_query_sync(query)

