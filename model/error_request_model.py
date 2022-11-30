from .base_model import BaseModel


class ErrorRequestModel(BaseModel):

    def __init__(self):
        super().__init__('public.error_request', 'c12b7985-1c5c-4ff2-8cb2-a172d68faec5')

    def insert(self, url: str, method: str, body: str, headers: str, exception: str):
        query = """
            insert into error_request (url, method, body, headers, status, exception)
            values (%s, %s, %s, %s, %s, %s)
            returning *;
        """

        return self.run_query_sync(query, [url, method, body, headers, 0, exception])
