# Generate new app for every content-creator when a new app code released

import logging
import sys
import time

import git
import psycopg2
import redis
from psycopg2 import extras

from config_reader import ConfigReader

rd = redis.Redis()

config = ConfigReader().read_config_file()

db_name = config['db_name']
db_user = config['db_user']
db_pass = config['db_pass']
db_port = config['db_port']
db_host = config['db_host']

QUERY = """
with cte as (
select distribution.id as distribution_id, app.id as app_id from distribution,
(select id, max(version_code) as version_code from app group by id order by version_code desc limit 1) app
where distribution.status = 1
)
insert into distribution_app
select uuid_generate_v4(), cte.distribution_id, cte.app_id, 0, null, now(), now() from cte
returning *;
"""

logger = logging.getLogger("BUILDER_LOGGER")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


logger.info("start git-puller worker")

while True:
    result = rd.lpop("GIT_NOTIFY")
    if not result:
        time.sleep(5)

    logger.info("start pulling gitlab")
    project_git = git.Repo(config['project_path'])
    origin = project_git.remotes.origin
    response = origin.pull()
    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port, host=db_host) as connection:
        connection.autocommit = True
        with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(QUERY)
            db_result = cursor.fetchall()
            logger.info("inserting to db completed")
    logger.info("pull completed")
    time.sleep(5)
