from .base_model import BaseModel
from uuid import uuid5

import hashlib


class ChannelAdminModel(BaseModel):

    def __init__(self):
        super().__init__('public.channel_admin', '7aa1c5f9-5062-47a3-a166-be7ededfad66')

    async def insert(self, username: str, password: str, name: str):
        id = str(uuid5(self.namespace, username))
        query = """
            insert into channel_admin (id, "username", "password", "name")
            values (%s, %s, %s, %s)
            on conflict (id) do update set updated_at=now()
            returning *;
        """

        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [id, username, password, name])

    async def get_by_username_and_password(self, username: str, password: str):
        query = """
            select id, "username", payment_account, payment_bank_name, credit_card_number, credit_card_name, "name"
                from public.channel_admin
            where username=%s and password=%s
        """

        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [username, password])

    async def update_status(self, id: str, status: int):
        query = """
            update channel_admin
            set status=%s
            where id=%s
            returning *;
        """

        return await self.run_query(query, [status, id])

    async def update_data(self, id: str, payment_account: str, payment_bank: str, credit_card_number: str,
                          credit_card_name: str):
        query = """
            update channel_admin
            set payment_account=%s, payment_bank_name=%s, credit_card_number=%s, credit_card_name=%s
            where id=%s
            returning *;
        """

        return await self.run_query(query, [payment_account, payment_bank, credit_card_number, credit_card_name, id])

    async def get_channel_admin_with_channels(self):
        query = """
            select channel_admin.id, username, payment_account, payment_bank_name, credit_card_number, credit_card_name, channel_admin.status,
                 channel_admin.name, json_agg(distinct distribution.*) as channels, channel_admin.created_at, channel_admin.updated_at from channel_admin
            left join distribution on channel_admin.id = distribution.channel_owner
            group by channel_admin.id
        """

        return await self.run_query(query)

    async def get_channel_success_transactions(self, channel_admin_id: str):
        query = """
            select channel_admin.id, channel_admin.username, channel_admin.payment_account,
                   channel_admin.payment_bank_name,
                   channel_admin.credit_card_number, channel_admin.credit_card_name,
                   channel_admin.status, channel_admin.created_at, channel_admin.updated_at, json_agg(trans.*) as transactions
            from channel_admin
            left join (
                select id, user_id, course_id, price from transaction
              where status=1 and keyword in (select id from distribution where channel_owner=%s)
              ) trans on true
            where channel_admin.id = %s
            group by channel_admin.id
        """

        return await self.run_query(query, [channel_admin_id, channel_admin_id])

    async def get_channel_admin_profile(self, admin_id: str):
        query = """
            with cte as (
                select channel_admin_id, sum(amount) as total_received from balance
                where channel_admin_id=%s
                group by balance.channel_admin_id
            ),
            cte2 as (
                select sum(price) as total_sell from transaction
                where status=1 and keyword in (select id from distribution where channel_owner=%s)
            )
            select channel_admin.id, username, payment_account, payment_bank_name, credit_card_number, credit_card_name,
                channel_admin.status, channel_admin.created_at, channel_admin.updated_at, json_agg(distinct distribution.*) as channels,
                cte2.total_sell, cte.total_received
            from channel_admin
            left join distribution on channel_admin.id = distribution.channel_owner
            left join cte on true
            left join cte2 on true
            where channel_admin.id = %s
            group by channel_admin.id, cte2.total_sell, cte.total_received
        """

        return await self.run_query(query, [admin_id, admin_id, admin_id])

    async def get_distribution_app(self, channel_admin_id: str):
        query = """
            select distribution_app.*, row_to_json(distribution.*) as distribution from distribution
            inner join distribution_app on distribution.id = distribution_app.distribution_id
            where channel_owner=%s
        """

        return await self.run_query(query, [channel_admin_id])

    async def find_by_username(self, username: str):
        query = """
            select username from channel_admin
            where username=%s
        """

        return await self.run_query(query, [username])

    async def get_channel_admin_balances(self, channel_admin_id: str):
        query = """
            select channel_admin.id, username, payment_account, payment_bank_name, credit_card_name, credit_card_number, status, name, channel_admin.created_at, channel_admin.updated_at, json_agg(balance.*) as balance from channel_admin
            left join balance on channel_admin.id = balance.channel_admin_id
            where channel_admin.id = %s
            group by channel_admin.id
        """

        return await self.run_query(query, [channel_admin_id])

    async def get_recoupment_account(self, channel_admin_id: str, from_date: str, to_date: str):
        query = """
            with user_distributions as (
              select id from distribution
              where channel_owner=%s
            )
            , transactions as (
              select *, %s::uuid as channel_admin_id from transaction
              where keyword in (select id from user_distributions) and status=1 and created_at >= %s and created_at < %s
            ), balances as (
              select * from balance
              where channel_admin_id=%s and created_at >= %s and created_at < %s
            )
            select channel_admin.*, json_agg(distinct balances.*) as balance, json_agg(distinct transactions.*) as
                transactions, sum(distinct transactions.price) as total_sell, sum(distinct balances.amount) as total_received from channel_admin
            left join transactions on transactions.channel_admin_id = channel_admin.id
            left join balances on balances.channel_admin_id = channel_admin.id
            where channel_admin.id = %s
            group by channel_admin.id
        """

        return await self.run_query(query, [channel_admin_id, channel_admin_id, from_date, to_date, channel_admin_id,
                                            from_date, to_date, channel_admin_id])

    async def change_password(self, channel_admin_id: str, password: str):
        query = """
            update channel_admin
            set password=%s, updated_at=now()
            where id=%s
            returning *;
        """
        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [password, channel_admin_id])

    async def find_by_id_and_password(self, channel_admin_id: str, password: str):
        query = """
            select * from channel_admin
            where id=%s and password=%s
        """

        password = hashlib.sha1(password.encode()).hexdigest()
        return await self.run_query(query, [channel_admin_id, password])

    async def get_channel_admin_and_distribution_status(self, distribution_id: str):
        query = """
            select distribution.status as  distribution_status, channel_admin.status as channel_admin_status
                from distribution
            inner join channel_admin on distribution.channel_owner = channel_admin.id
            where distribution.id=%s
        """

        return await self.run_query(query, [distribution_id])

    async def disable_all_channel_admin_distributions(self, channel_admin_id: str):
        query = """
            update distribution
            set status=2
            where channel_owner=%s
        """

        return await self.run_query(query, [channel_admin_id])
