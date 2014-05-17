# -*- coding: utf-8 -*-
# Copyright (c) 2014 Eric Smith
import logging
from logging.handlers import RotatingFileHandler
import sys


def setup_stdout(level):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    handler.setLevel(level)
    logging.getLogger().addHandler(handler)


def setup_file(filename, level):
    handler = RotatingFileHandler(filename, maxBytes=102400, backupCount=5)
    fmt = '%(asctime)s %(levelname)-7s %(message)s'
    handler.setFormatter(logging.Formatter(fmt))
    handler.setLevel(level)
    logging.getLogger().addHandler(handler)


logging.getLogger().setLevel(logging.NOTSET)

