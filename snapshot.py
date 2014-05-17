# -*- coding: utf-8 -*-
# Copyright (c) 2014 Eric Smith
from datetime import datetime
import logging
import os
import requests
import time
import sys
from config import Config
import log

URL_BASE = 'https://alert.logitech.com/services'
PERIOD = 10  # 60
CHUNK_SIZE = 4096

logger = logging.getLogger()


def main():
    config = load_config()
    setup_directories(config)
    log.setup_stdout(logging.INFO)
    log.setup_file(config.logfile, logging.DEBUG)
    token = authenticate(config.username, config.password)
    if token:
        headers = {'X-Authorization': token}
        url = URL_BASE + '/camera2.svc/{}/snapshotviewable'.format(config.mac)
        snapshot_loop(url, headers, config.output)


def load_config():
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    config = Config(config_file)
    config.logfile = os.path.expanduser(config.logfile)
    config.output = os.path.expanduser(config.output)
    return config


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
        </AuthInfo>""".format(username, password)  # todo: escape
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, body, headers=headers)
    if response.ok:
        return response.headers['X-Authorization-Token']
    else:
        logger.error('Authentication failed - ' + str(response))


def snapshot_loop(url, headers, output):
    while True:
        filename = get_filename(output)
        download(url, filename, headers)
        time.sleep(PERIOD)


def get_filename(output):
    now = datetime.now()
    return os.path.join(output, now.strftime('%Y-%m-%dT%H%M%S') + '.jpg')


def download(url, filename, headers):
    logger.info(filename)
    with open(filename, 'wb') as handle:
        response = requests.get(url, stream=True, headers=headers)
        if response.ok:
            for block in response.iter_content(CHUNK_SIZE):
                if not block:
                    break
                handle.write(block)
        else:
            logger.error('Download failed - ' + str(response))


if __name__ == '__main__':
    main()
