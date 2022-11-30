from .base_model import BaseModel


class DistributionModel(BaseModel):

    def __init__(self):
        super().__init__('public.distribution', 'd9cdc112-4588-406f-8911-9af69d98690f')

    async def insert(self, name: str, platform: str, channel_id: str, channel_owner: str):
        query = """
            insert into public.distribution (name, platform, channel_id, channel_owner)
            values (%s, %s, %s, %s)
            on conflict (platform, channel_id) do update set updated_at=now()
            returning *;
        """

        return await self.run_query(query, [name, platform, channel_id, channel_owner])

    def get_all_active_sync(self):
        query = """
            select * from public.distribution
            where status=1
        """

        return self.run_query_sync(query)

    async def find_by_platform_and_channel_id(self, platform: str, channel_id: str):
        query = """
            select * from public.distribution
            where channel_id=%s and platform=%s
        """

        return await self.run_query(query, [channel_id, platform])

    async def get_by_channel_admin_id(self, channel_admin_id: str):
        query = """
            select channel_admin.id, channel_admin.username, channel_admin.payment_account,
                   channel_admin.payment_bank_name,
                   channel_admin.credit_card_number, channel_admin.credit_card_name,
                   channel_admin.status, channel_admin.created_at, channel_admin.updated_at,
                   json_agg(distribution.*) as distribution
            from channel_admin
            left join distribution on channel_admin.id = distribution.channel_owner
            where channel_admin.id = %s
            group by channel_admin.id
        """

        return await self.run_query(query, [channel_admin_id])

    async def update_status(self, id: str, status: int):

        query = """
            update public.distribution
            set status=%s
            where id=%s
            returning *;
        """

        return await self.run_query(query, [status, id])

    async def get_by_owner(self, owner_id: str):
        query = """
            select * from public.distribution
            where channel_owner=%s
        """

        return await self.run_query(query, [owner_id])

    async def get_latest_app(self, distribution_id: str):
        query = """
            select version_code, link from distribution_app
            inner join app on distribution_app.app_id = app.id
            where distribution_app.distribution_id = %s
            order by app.created_at desc
            limit 1
        """

        return await self.run_query(query, [distribution_id])

    async def insert_new_app_version(self, version_code: int):
        query = """
            insert into app(version_code)
            values (%s)
            returning *;
        """

        return await self.run_query(query, [version_code])

    async def insert_dist_apps(self):
        query = """
            with cte as (
                select distribution.id as distribution_id, app.id as app_id from distribution,
                (select id, max(version_code) as version_code from app group by id order by version_code desc limit 1) app
                where distribution.status = 1
            )
            insert into distribution_app
            select uuid_generate_v4(), cte.distribution_id, cte.app_id, 0, null, now(), now() from cte
            returning *;
        """

        return await self.run_query(query)

    async def insert_dist_by_dist_id(self, distribution_id: str):
        query = """
            with cte as (
                select distribution.id as distribution_id, app.id as app_id from distribution,
                (select id, max(version_code) as version_code from app group by id order by version_code desc limit 1) app
                where distribution.id = %s
            )
            insert into distribution_app
            select uuid_generate_v4(), cte.distribution_id, cte.app_id, 0, null, now(), now() from cte
            returning *;
        """

        return await self.run_query(query, [distribution_id])

    def update_analytics_sync(self, dist_id: str, total_users: str, total_installed: str):
        query = """
            update distribution
            set user_count=%s, installed=%s
            where id=%s
            returning *;
        """

        return self.run_query_sync(query, [total_users, total_installed, dist_id])


