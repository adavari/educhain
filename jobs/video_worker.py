# Encode uploaded video files.

import asyncio
import json
import os
import subprocess
import sys
import time
import logging

import ffmpeg

from model.course_model import CourseModel
from model.section_model import SectionModel

config = {}

cdn_path = ""


def get_duration(input_file):
    result = subprocess.Popen('ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(input_file),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = result.communicate()
    return int(float(output[0].decode("utf-8").replace('\n', '')))


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

logger = logging.getLogger("BUILDER_LOGGER")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


async def run():
    await SectionModel().update_all_chapter_status(0, 1)

    while True:
        time.sleep(5)
        data = await CourseModel().find_one_by_status(0)

        if data is not None and len(data) == 1:
            course_id = data[0]['id']

            logger.info("Find course {}".format(course_id))

            sections = await SectionModel().find_by_course_id_and_status_and_type(course_id, 0, 1)

            if sections is not None and len(sections) > 0:

                for section in sections:
                    time.sleep(1)
                    section_id = section['id']

                    logger.info("start converting section {} from {}".format(section_id, course_id))

                    await SectionModel().update_status(section_id, 1)
                    in_file = raw_path + '/' + section['raw_file']
                    rand_name = get_random_filename() + '.mp4'
                    out_file = cdn_path + '/' + rand_name

                    stream = ffmpeg.input(in_file)
                    stream = ffmpeg.output(stream, out_file)
                    ffmpeg.run(stream)

                    size = os.path.getsize(out_file)
                    duration = get_duration(out_file)

                    logger.info("converting {} completed. copied to {}".format(section_id, out_file))

                    await SectionModel().publish(section_id, rand_name, duration, size)

                logger.info("course published {} ".format(course_id))
                await CourseModel().publish_course(course_id)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(run())
