from .base_model import BaseModel


class BalanceModel(BaseModel):

    def __init__(self):
        super().__init__('public.balance', 'f39778f9-d86a-417d-a886-31cc5f6db2dc')

    async def insert(self, channel_admin_id: str, amount: int):
        query = """
            insert into balance(channel_admin_id, amount)
            values(%s, %s)
            returning *;
        """

        return await self.run_query(query, [channel_admin_id, amount])

    async def find_by_channel_admin_id(self, channel_admin_id: str):
        query = """
            select channel_admin.id, channel_admin.username, channel_admin.payment_account,
                   channel_admin.payment_bank_name,
                   channel_admin.credit_card_number, channel_admin.credit_card_name,
                   channel_admin.status, channel_admin.created_at, channel_admin.updated_at,
                   json_agg(balance.*) as balance
            from channel_admin
            left join balance on channel_admin.id = balance.channel_admin_id
            where channel_admin.id = %s
            group by channel_admin.id;        
        """

        return await self.run_query(query, [channel_admin_id])
