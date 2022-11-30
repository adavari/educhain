from .base_model import BaseModel


class AnalyticsModel(BaseModel):

    def __init__(self):
        super().__init__('public.analytics', '3a4cb3c7-db2b-4e52-b007-b7adc8fe7f50')

    async def insert(self, keyword: str):
        query = """
            insert into public.analytics (keyword)
            values (%s)
            returning *;
        """

        return await self.run_query(query, [keyword])

    def get_installed_count(self, dist_id: str):
        query = """
            select count(analytics.*) as total_install from analytics
            where keyword=%s and analytics_type=1
        """

        return self.run_query_sync(query, [dist_id])
