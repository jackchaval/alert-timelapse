# -*- coding: utf-8 -*-
# Copyright (c) 2014 Eric Smith
import json


class Config(dict):
    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self._load()

    def _load(self):
        with open(self.filename, 'r') as handle:
            self.__dict__ = json.load(handle)

    def __getattr__(self, key):
        return self[key]
