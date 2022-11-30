from .base_model import BaseModel
from uuid import uuid5
import uuid


class CourseModel(BaseModel):

    def __init__(self):
        super().__init__('public.course', '26241b5e-423e-404d-a5cb-d230d764fa3b')

    async def insert(self, titls: str, description: str, price: int, teacher: str, icon: str):
        query = """
            insert into public.course (title, description, price, teacher, course_icon)
            values (%s, %s, %s, %s, %s)
            returning course.id, course.title, course.description, course.status, course.created_at, course.updated_at,
                price, teacher, encode(aes_key, 'hex') as aes_key, encode(aes_iv, 'hex') as aes_iv, course_icon;
        """

        return await self.run_query(query, [titls, description, price, teacher, icon])

    async def find_by_status(self, status: int):
        query = """
            select * from public.course
            where  status=%s and exists((select course_id from section where course_id = course.id))
            order by random()
        """

        return await self.run_query(query, [status])

    async def find_one_by_status(self, status: int):
        query = """
                    select * from public.course
                    where  status=%s and exists((select course_id from section where course_id = course.id))
                    order by random()
                    limit 1
                """

        return await self.run_query(query, [status])

    async def update_status(self, course_id: str, status: int):
        query = """
            update public.course
            set status=%s
            where id=%s
        """

        return await self.run_query(query, [status, course_id])

    async def publish_course(self, course_id: str):
        query = """
            update public.course
            set status=1
            where id=%s
        """

        await self.run_query(query, [course_id])

    async def get_published_courses(self):
        query = """
            select course.id, course.title, course.description, course.status, course.created_at, course.updated_at,
                price, teacher, encode(aes_key, 'hex') as aes_key, encode(aes_iv, 'hex') as aes_iv,
                json_agg(distinct section.*) as sections, course_icon from course
            inner join section on course.id = section.course_id
            where course.status=2
            group by course.id
        """

        return await self.run_query(query)

    async def get_by_id(self, course_id: str):
        query = """
            select course.id, course.title, course.description, course.status,
                course.created_at, course.updated_at, price, teacher, encode(aes_key, 'hex') as aes_key,
                encode(aes_iv, 'hex') as aes_iv, course_icon from course
            where id=%s
        """
        return await self.run_query(query, [course_id])

    async def get_user_course(self, user_id: str):
        query = """
            with user_courses as (
              select *
              from user_course
              where user_id = %s
            ),
            sections as (select section.id,
                                     section.title,
                                     section.description,
                                     section_type,
                                     section.course_id,
                                     section.ordering,
                                     section.size,
                                     section.duration,
                                     (case
                                        when section.is_free = true or
                                             exists(select * from user_courses where user_courses.course_id = section.course_id)
                                          then section.file
                                        else null end) as file,
                                     created_at,
                                     updated_at
                              from section
                              where status = 4
                 )
            select course.id,
                   course.title,
                   course.description,
                   course.status,
                   course.created_at,
                   course.updated_at,
                   price,
                   teacher,
                   encode(aes_key, 'hex')                             as aes_key,
                   encode(aes_iv, 'hex')                              as aes_iv,
                   course_icon,
                   json_agg(distinct sections.*)                      as sections,
                   exists((select course_id
                           from user_courses
                           where user_courses.course_id = course.id)) as is_bought
            from course
                   inner join sections on sections.course_id = course.id
            where course.status = 2
            group by course.id
        """

        return await self.run_query(query, [user_id])

    async def get_all_course_with_sections(self):
        query = """
            select course.id, course.title, course.description, course.status,
              course.created_at, course.updated_at, price, teacher, encode(aes_key, 'hex') as aes_key,
              encode(aes_iv, 'hex') as aes_iv, json_agg(distinct section.*) as sections, course_icon from course
            left join section on course.id = section.course_id
            group by course.id
        """

        return await self.run_query(query)

    async def update_course_by_id(self, course_id: str, title: str, description: str, price: int, teacher: str):
        query = """
            update public.course
            set title=%s, description=%s, price=%s, teacher=%s
            where id=%s
            returning course.id, course.title, course.description, course.status, course.created_at,
                course.updated_at, price, teacher, course_icon,
                encode(aes_key, 'hex') as aes_key, encode(aes_iv, 'hex') as aes_iv;
        """

        return await self.run_query(query, [title, description, price, teacher, course_id])


    async def update_course_by_id_with_icon(self, course_id: str, title: str, description: str, price: int, teacher: str, icon: str):
        query = """
            update public.course
            set title=%s, description=%s, price=%s, teacher=%s, course_icon=%s
            where id=%s
            returning course.id, course.title, course.description, course.status, course.created_at,
                course.updated_at, price, teacher, course_icon,
                encode(aes_key, 'hex') as aes_key, encode(aes_iv, 'hex') as aes_iv;
        """

        return await self.run_query(query, [title, description, price, teacher, icon, course_id])

    async def insert_user_course(self, course_id: str, user_id: str):
        query = """
            insert into public.user_course (id, user_id, course_id)
            values(%s, %s, %s)
            on conflict (id) do update set updated_at=now()
            returning *;
        """

        id = str(uuid5(uuid.UUID('4269a03b-4759-431e-8a44-a8f0833acba1'), course_id + '-' + user_id))
        return await self.run_query(query, [id, user_id, course_id])


    def insert_user_course_sync(self, course_id: str, user_id: str):
        query = """
            insert into public.user_course (id, user_id, course_id)
            values(%s, %s, %s)
            on conflict (id) do nothing
            returning *;
        """

        id = str(uuid5(uuid.UUID('4269a03b-4759-431e-8a44-a8f0833acba1'), course_id + '-' + user_id))
        return self.run_query_sync(query, [id, user_id, course_id])

    async def get_course_topics(self, course_id: str):
        query = """
            select * from topic where course_id=%s
        """

        return await self.run_query(query, [course_id])

    async def get_course_faq(self, course_id: str):
        query = """
            select * from faqs where course_id=%s
        """

        return await self.run_query(query, [course_id])

    async def get_list_question_by_course_id(self, course_id: str, user_id: str):
        # query = """
        #     select coalesce(json_agg(distinct faqs.*) filter (where faqs.id is not null), '[]')  as faq,
        #     coalesce(json_agg(distinct ts.*) filter (where ts.id is not null), '[]') as messages from faqs
        #     left join ( select * from public.message where course_id=%s and user_id=%s) as ts on true
        #     where faqs.course_id = %s
        # """

        query = """
            select (select coalesce(json_agg(row_to_json(message.*)) filter ( where message.id is not null ), '[]') as messages
                from message  where course_id=%s and user_id=%s) as messages,
            (select coalesce(json_agg(row_to_json(faqs.*)) filter ( where faqs.id is not null ), '[]') as faq from faqs where course_id=%s)
        """

        return await self.run_query(query, [course_id, user_id, course_id])

    async def delete_by_id(self, course_id: str):
        query = """
            delete from course
            where id=%s
        """

        await self.run_query(query, [course_id])
