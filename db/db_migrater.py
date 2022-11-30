import logging
import os

import psycopg2
import redis
from psycopg2 import extras
r = redis.Redis()

db_name = r.get('name').decode()
db_user = r.get('user').decode()
db_pass = r.get('pass').decode()
db_port = r.get('port').decode()

connection = psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port)
if connection:
    connection.autocommit = True
    files = os.listdir('../migrations/')
    files.sort()
    for f in files:
        logging.log(f)
        with open('migrations/' + f, 'r') as sql_file:
            try:
                sql = sql_file.read()
                cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
                cursor.execute(sql)

                connection.commit()
                cursor.close()
            except Exception as e:
                logging.error(str(e))
            sql_file.close()

    connection.close()


else: 
    logging.log("can't connect to database !")