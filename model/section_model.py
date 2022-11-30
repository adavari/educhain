from .base_model import BaseModel


class SectionModel(BaseModel):

    def __init__(self):
        super().__init__('public.section', '3ef6236c-484b-4f7c-af3d-81b10ea5acf1')

    async def insert(self, title: str, description: str, course_id: str, ordering: int, raw_file: str,
                     section_type: int, is_free: bool):
        query = """
            insert into public.section (title, description, course_id, ordering, raw_file, section_type, is_free)
            values (%s, %s, %s, %s, %s, %s, %s)
            returning *;
        """

        return await self.run_query(query, [
            title, description, course_id, ordering, raw_file, section_type, is_free
        ])

    async def update_all_chapter_status(self, to: int, from_status: int):
        query = """
            update public.section
            set status=%s
            where status=%s
        """

        await self.run_query(query, [to, from_status])

    async def find_by_course_id_and_status(self, course_id: str, status: int):
        query = """
            select * from public.section
            where course_id=%s and status=%s
        """

        return await self.run_query(query, [course_id, status])

    async def find_by_course_id_and_status_and_type(self, course_id: str, status: int, section_type: int):
        query = """
            select * from public.section
            where course_id=%s and status=%s and section_type=%s
        """

        return await self.run_query(query, [course_id, status, section_type])

    async def update_status(self, section_id: str, status: int):
        query = """
            update public.section
            set status=%s
            where id=%s
        """

        await self.run_query(query, [status, section_id])

    async def publish(self, section_id: str, name: str, duration: int, size: int):
        query = """
            update public.section
            set status=2, size=%s, duration=%s, file=%s
            where id=%s
        """

        await self.run_query(query, [size, duration, name, section_id])

    async def find_by_course_id(self, course_id: str):
        query = """
            select course.id, course.title, course.description, course.status, course.created_at, course.updated_at, price,
            teacher, encode(aes_key, 'hex') as aes_key, encode(aes_iv, 'hex') as aes_iv, course_icon,
                course.created_at,course.created_at, json_agg(section.*) as sections from course
            left join section on course.id = section.course_id
            where course.id = %s
            group by course.id
        """

        return await self.run_query(query, [course_id])

    async def find_by_course_id_v2(self, course_id: str):
        query = """
            select * from public.section
            where course_id=%s
        """

        return await self.run_query(query, [course_id])

    async def update_by_id(self, section_id: str, title: str, description: str, course_id: str, ordering: int,
                           section_type: int, is_free: bool):
        query = """
            update public.section 
            set title=%s, description=%s, course_id=%s, ordering=%s, section_type=%s, is_free=%s
            where id=%s
            returning *;
        """

        return await self.run_query(query, [
            title, description, course_id, ordering, section_type, is_free, section_id
        ])
