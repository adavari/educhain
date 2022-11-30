import logging
import os
import select
from uuid import UUID

import psycopg2
from psycopg2 import extras


class BaseModel:
    table_name: str = ""
    namespace = ""

    def __init__(self, table_name: str, namespace: str):
        self.table_name = table_name
        self.namespace = UUID(namespace)

    async def run_query(self, query: str, data: list = None):
        db_name = os.getenv('name')
        db_user = os.getenv('user')
        db_pass = os.getenv('pass')
        db_port = os.getenv('port')
        db_host = os.getenv("host")

        kwargs = {'async': 1}
        with psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port, host=db_host, **kwargs) \
                as connection:
            await self.wait(connection)
            if not connection:
                return None
            with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                if data is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, data)
                await self.wait(connection)
                result = cursor.fetchall()
                return result

    def run_query_sync(self, query: str, data: list = None):
        db_name = os.getenv('name')
        db_user = os.getenv('user')
        db_pass = os.getenv('pass')
        db_port = os.getenv('port')
        db_host = os.getenv("host")

        with psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port, host=db_host) as connection:
            if not connection:
                return None
            with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                if data is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, data)
                connection.commit()
                result = cursor.fetchall()
                return result

    async def find_all(self):
        query = """ select * from {} """.format(self.table_name)
        return await self.run_query(query)

    async def find_by_id(self, id: str):
        query = """select * from {} where id = %s""".format(self.table_name)
        return await self.run_query(query, [id])

    async def delete_by_id(self, id: str):
        query = """
            delete from {}
            where id=%s
        """.format(self.table_name)
        return await self.run_query(query, [id])

    async def wait(self, conn):
        while True:
            state = conn.poll()
            if state == psycopg2.extensions.POLL_OK:
                break
            elif state == psycopg2.extensions.POLL_WRITE:
                select.select([], [conn.fileno()], [])
            elif state == psycopg2.extensions.POLL_READ:
                select.select([conn.fileno()], [], [])
            else:
                raise psycopg2.OperationalError("poll() returned %s" % state)
