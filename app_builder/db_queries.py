REMOVE_UNCOMPLETED_BUILDINGS_STATUS = """
update distribution_app
set status=0
where status=1
returning *;
"""

GET_BUILD_QUEUES = """
select * from distribution_app
where status=0;
"""

UPDATE_DISTRIBUTION_APP_STATUS = """
update distribution_app
set status=%s
where id=%s
"""

UPDATE_APP_LINK = """
update distribution_app
set link=%s
where id=%s
"""
