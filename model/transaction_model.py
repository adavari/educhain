from .base_model import BaseModel


class TransactionModel(BaseModel):

    def __init__(self):
        super().__init__('public.transaction', '42d88e65-924a-4da8-b97a-7e3baa36ff6d')

    async def insert(self, transaction_code: str, user_id: str, course_id: str, response_log: str, price: int,
                     keyword: str):
        query = """
            insert into public.transaction (transaction_code, user_id, course_id, response_log, price, keyword)
            values(%s, %s, %s, %s, %s, %s)
            returning *;
        """

        return await self.run_query(query, [transaction_code, user_id, course_id, response_log, price, keyword])

    async def update_transaction_status(self, id: str, status: int):
        query = """
            update transaction
            set status=%s, validated_at=now(), updated_at=now()
            where id=%s
            returning *;
        """

        return await self.run_query(query, [status, id])

    def update_transaction_status_sync(self, id: str, status: int):
        query = """
            update transaction
            set status=%s, validated_at=now(), updated_at=now()
            where id=%s
            returning *;
        """

        return self.run_query_sync(query, [status, id])

    async def get_transaction_by_user_id(self, user_id: str):
        query = """
            with cte2 as (
              select course.id, course.title, course.description, course.status, course.created_at, course.updated_at, price, teacher, encode(aes_key, 'hex') as aes_key, encode(aes_iv, 'hex') as aes_iv from course
            )
            ,cte as (
              select transaction.*,
                 row_to_json(cte2.*) as course from transaction
              inner join cte2 on transaction.course_id = cte2.id
            )
            select users.id, users.username, users.sure_name, users.email, users.keyword, json_agg(cte.*) as transactions from users
            left join cte on cte.user_id = users.id
            where users.id=%s
            group by users.id;
        """

        return await self.run_query(query, [user_id])

    async def get_all_transactions(self, user_id: str):
        query = """
            select transaction.*, json_agg(course.*) as course, json_agg(users.*) as users from public.transaction
            left join course on transaction.course_id = course.id
            inner join users on transaction.user_id = users.id
            group by transaction.id;
        """

        return await self.run_query(query)

    async def get_by_distribution_id(self, distribution_id: str):
        query = """
            select distribution.*, json_agg(transaction.*) as transactions from distribution
            left join transaction on distribution.id = transaction.keyword
            where distribution.id = %s
            group by distribution.id
        """

        return await self.run_query(query, [distribution_id])

    def get_unvalidated_transactions(self):
        query = """
            select * from transaction
            where (status is null or status = 0) and created_at < now() -  interval '15 minutes'
        """

        return self.run_query_sync(query)

    def get_transactions_by_status_sync(self, status: int):
        query = """
            select * from transaction
            where status=%s
        """

        return self.run_query_sync(query, [status])
