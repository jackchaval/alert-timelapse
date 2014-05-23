# -*- coding: utf-8 -*-
# Copyright (c) 2014 Eric Smith
from datetime import datetime, timedelta
from xml.sax.saxutils import escape
import logging
import os
import time
import sys

import requests

from config import Config
import log


URL_BASE = 'https://alert.logitech.com/services'
PERIOD_SECONDS = 10  # 60
CHUNK_SIZE = 4096

logger = logging.getLogger()
session = requests.Session()


def main():
    config = load_config()
    setup_directories(config)
    log.setup_stdout(logging.INFO)
    log.setup_file(config.logfile, logging.DEBUG)
    token = authenticate(config.username, config.password)
    if token:
        headers = {'X-Authorization': token}
        url = URL_BASE + '/camera2.svc/{}/snapshotviewable'.format(config.mac)
        snapshot_loop(url, headers, config)


def load_config():
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    config = Config(config_file)
    config.logfile = os.path.expanduser(config.logfile)
    config.output = os.path.expanduser(config.output)
    config.start_time = parse_time(config.get('start'))
    config.stop_time = parse_time(config.get('stop'))
    return config


def parse_time(time_str):
    if time_str:
        return datetime.strptime(time_str, '%H:%M').time()
    return None


def setup_directories(config):
    log_directory = os.path.dirname(config.logfile)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    if not os.path.exists(config.output):
        os.makedirs(config.output)


def authenticate(username, password):
    logger.info('Authenticating as ' + username)
    url = URL_BASE + '/membership.svc/authenticate'
    body = """<AuthInfo>
        <UserName>{}</UserName>
        <Password>{}</Password>
        </AuthInfo>""".format(escape(username), escape(password))
    headers = {'Content-Type': 'application/xml'}
    response = session.post(url, body, headers=headers)
    if response.ok:
        return response.headers['X-Authorization-Token']
    else:
        logger.error('Authentication failed - ' + str(response))


def snapshot_loop(url, headers, config):
    while True:
        time.sleep(get_sleep_time(config))
        filename = get_filename(config.output)
        download(url, filename, headers)


def get_filename(output):
    global _image_counter
    filename = None
    now = datetime.now()
    daily_dir = os.path.join(output, now.strftime('%Y-%m-%d'))
    if not os.path.exists(daily_dir):
        os.makedirs(daily_dir)
        _image_counter = 0
    elif _image_counter == -1:
        _image_counter = 0
        file_exists = True
        while file_exists:
            filename = next_filename(daily_dir)
            file_exists = os.path.exists(filename)
        return filename
    return next_filename(daily_dir)


def next_filename(daily_dir):
    global _image_counter
    filename = os.path.join(daily_dir, '{0:04d}.jpg'.format(_image_counter))
    _image_counter += 1
    return filename


_image_counter = -1


def download(url, filename, headers):
    logger.info(filename)
    with open(filename, 'wb') as handle:
        response = session.get(url, stream=True, headers=headers)
        if response.ok:
            for block in response.iter_content(CHUNK_SIZE):
                if not block:
                    break
                handle.write(block)
        else:
            logger.error('Download failed - ' + str(response))


def get_sleep_time(config):
    delta = timedelta(seconds=PERIOD_SECONDS)
    if config.start_time and config.stop_time:
        now = datetime.now()
        start_today = time_today(now, config.start_time)
        stop_today = time_today(now, config.stop_time)
        start_tomorrow = time_tomorrow(now, config.start_time)
        if now < start_today:
            delta = start_today - now
        elif now > stop_today:
            delta = start_tomorrow - now
        if delta.total_seconds() > PERIOD_SECONDS:
            logger.info('Sleeping {} to next start time.'.format(delta))
    return delta.total_seconds()


def time_today(now, t):
    return datetime(now.year, now.month, now.day, t.hour, t.minute)


def time_tomorrow(now, t):
    return time_today(now, t) + timedelta(days=1)


if __name__ == '__main__':
    main()
