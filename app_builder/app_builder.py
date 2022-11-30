import logging
import os
import subprocess
import sys
import time
from shutil import copyfile

import psycopg2
from psycopg2 import extras

import db_queries
from config_reader import ConfigReader

config = ConfigReader().read_config_file()


def put_keyword_to_source(keyword: str):
    path = config['project_path'] + '/app/src/main/assets/keyword.txt'
    with open(path, 'w') as file:
        file.write(keyword)


def build_with_gradle():
    command = "{}/gradlew -p {} clean assembleRelease".format(config['project_path'], config['project_path'])
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return not error


def rename_release_build(dist_id):
    temp_apk_path = config['project_path'] + '/app/build/outputs/apk/release/app-release.apk'
    apk_path = config['project_path'] + '/app/build/outputs/apk/release/{}.apk'.format(dist_id)
    copyfile(temp_apk_path, apk_path)
    os.remove(temp_apk_path)
    return apk_path


def update_db_status(i, status):
    cursor.execute(db_queries.UPDATE_DISTRIBUTION_APP_STATUS, [status, i])


def scp_file(app_name):
    command = "scp -i {} {} kermit:/var/www/html/".format(config['private_key_path'], app_name)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return not error


def set_link(app_name, i):
    cursor.execute(db_queries.UPDATE_APP_LINK, [app_name, i])


def pull_git():
    # logger.info("start pulling gitlab")
    # project_git = git.Repo(config['project_path'])
    # origin = project_git.remotes.origin
    # response = origin.pull()
    # return response
    command = "git -C {} pull origin master".format(config['project_path'])
    process = subprocess.Popen(command.split())
    output, error = process.communicate()

    return not error

db_name = config['db_name']
db_user = config['db_user']
db_pass = config['db_pass']
db_port = config['db_port']
db_host = config['db_host']

logger = logging.getLogger("BUILDER_LOGGER")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

connection = psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port, host=db_host)
if not connection:
    logger.error("can't connect to database")
    exit(1)

connection.autocommit = True
cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
cursor.execute(db_queries.REMOVE_UNCOMPLETED_BUILDINGS_STATUS)
cursor.fetchall()
logger.info("connection established. starting worker ...")

while True:
    time.sleep(30)
    cursor.execute(db_queries.GET_BUILD_QUEUES)
    result = cursor.fetchall()
    if result is not None and len(result) > 0:
        for r in result:
            pull_git()
            logger.info("pull from gitlab completed")
            dist_id = r['distribution_id']
            update_db_status(r['id'], 1)
            put_keyword_to_source(dist_id)
            logger.info("App {} start build".format(r['id']))
            is_built = build_with_gradle()
            if is_built:
                logger.info("App {} was build".format(r['id']))
                app_name = rename_release_build(r['id'])
                logger.info("start scp of {}".format(r['id']))
                scp_file(app_name)
                logger.info("{} scp completed".format(r['id']))
                update_db_status(r['id'], 2)
                logger.info("{} status updated".format(r['id']))
                set_link("{}.apk".format(r['id']), r['id'])
                logger.info("{} link generated".format(r['id']))
            else:
                update_db_status(r['id'], 0)

