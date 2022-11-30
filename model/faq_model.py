from .base_model import BaseModel


class FaqModel(BaseModel):

    def __init__(self):
        super().__init__('public.faqs', '98205a89-4b2d-4da2-a0e6-c86c9a46795f')

    async def insert(self, question: str, answer: str):
        query = """
            insert into public.faqs (queston, answer)
            values(%s, %s)
            returning *;
        """

        return await self.run_query(query, [question, answer])

    async def insert_with_course_id(self, question: str, answer: str, course_id: str):
        query = """
            insert into public.faqs (queston, answer, course_id)
            values(%s, %s, %s)
            returning *;
        """

        return await self.run_query(query, [question, answer, course_id])

    async def update_by_id(self, faq_id: str, question: str, answer: str):
        query = """
            update public.faqs
            set queston=%s, answer=%s
            where id=%s
            returning *;
        """

        return await self.run_query(query, [question, answer, faq_id])

    async def update_by_id_with_course_id(self, faq_id: str, question: str, answer: str, course_id: str):
        query = """
            update public.faqs
            set queston=%s, answer=%s, course_id=%s
            where id=%s
            returning *;
        """

        return await self.run_query(query, [question, answer, faq_id, course_id])

    async def get_all_with_course(self):
        query = """
            with cte as (
              select course.id,
                     course.title,
                     course.description,
                     course.status,
                     course.created_at,
                     course.updated_at,
                     price,
                     teacher,
                     encode(aes_key, 'hex') as aes_key,
                     encode(aes_iv, 'hex')  as aes_iv
              from course
            )
            select faqs.*, row_to_json(cte.*) as course from faqs
            left join cte on faqs.course_id = cte.id
        """

        return await self.run_query(query)

    async def get_all_public_faqs(self):
        query = """
            select * from faqs
            where course_id is null
        """

        return await self.run_query(query)
