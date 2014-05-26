# -*- coding: utf-8 -*-
# Copyright (c) 2014 Eric Smith

import logging
import os
import subprocess
import sys

import log
from config import Config


def main():
    config = load_config()
    setup_directories(config)
    log.setup_stdout(logging.INFO)
    log.setup_file(config.logfile, logging.DEBUG)
    snapshots = os.path.join(config.input, '2014-05-24')
    video_file = os.path.join(config.output, '2014-05-24.mp4')
    create_video(snapshots, video_file)


def load_config():
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    config = Config(config_file)
    config.logfile = os.path.expanduser(config.logfile)
    config.input = os.path.join(os.path.expanduser(config.output), 'snapshot')
    config.output = os.path.join(os.path.expanduser(config.output), 'video')
    return config


def setup_directories(config):
    log_directory = os.path.dirname(config.logfile)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    if not os.path.exists(config.output):
        os.makedirs(config.output)


def create_video(snapshots, video_file):
    args = [
        'ffmpeg',
        '-i', '%04d.jpg',  # input files (4 zero-padded digits)
        '-loglevel', 'debug',
        video_file
    ]
    subprocess.call(args, cwd=snapshots)


if __name__ == '__main__':
    main()