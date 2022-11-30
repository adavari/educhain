# Encrypt uploaded files

import asyncio
import json
import logging
import os
import time
from shutil import copyfile

from model.course_model import CourseModel
from model.section_model import SectionModel
from utils.encryptor import encrypt_file

config = {}
cdn_path = ""


def get_random_filename():
    return str(int(round(time.time() * 1000)) - 1560000000000)


def read_config_file(filename):
    global config
    global cdn_path
    with open(filename, 'r') as config_file:
        con = config_file.read()
        config = json.loads(con)
        cdn_path = config['cdn']['path']


read_config_file(os.getenv("KERMIT_ROOT") + '/config.json')
raw_path = config['cdn']['raw_path']


async def run():
    await SectionModel().update_all_chapter_status(2, 3)

    while True:
        logging.log("sleeping :)")
        time.sleep(5)
        data = await CourseModel().find_one_by_status(1)

        if data is not None and len(data) == 1:
            course_id = data[0]['id']

            key = data[0]['aes_key']
            iv = data[0]['aes_iv']

            sections = await SectionModel().find_by_course_id_and_status(course_id, 2)

            if sections is not None and len(sections) > 0:

                for section in sections:
                    time.sleep(1)
                    section_id = section['id']

                    await SectionModel().update_status(section_id, 3)
                    in_file = cdn_path + '/' + section['file']
                    temp_file = get_random_filename()
                    out_file = cdn_path + '/' + temp_file

                    encrypt_file(bytes(key), bytes(iv), in_file, out_file)

                    os.remove(in_file)
                    copyfile(out_file, in_file)
                    os.remove(out_file)
                    await SectionModel().update_status(section_id, 4)

                await CourseModel().update_status(course_id, 2)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(run())
