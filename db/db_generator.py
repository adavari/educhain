import logging

from psycopg2.pool import SimpleConnectionPool
import json
from psycopg2 import extras

config = {}
sql = ""


def read_config_file(filename):
    global config
    with open(filename, 'r') as config_file:
        con = config_file.read()
        config = json.loads(con)


def read_sql_file():
    global sql
    with open('kermit.sql', 'r') as config_file:
        sql = config_file.read()


read_config_file("config.json")
read_sql_file()
pool = SimpleConnectionPool(1, 20, user=config['db']['user'], password=config['db']['pass'],
                            host=config['db']['host'], port=config['db']['port'],
                            database=config['db']['name'])

connection = pool.getconn()
if connection:

    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute(sql)

    connection.commit()
    cursor.close()
    connection.close()

else:
    logging.log("cant connect to database!")
