#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser

class config(object):
    def __init__(self, path):
        self.path = path

    def read(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.path)
        return parser

    def getDict(self):
        parser = self.read()
        config_dict = {}
        for section in parser.sections():
            config_dict[section] = {}
            for option in parser.options(section):
                config_dict[section][option] = parser.get(section, option)
        return config_dict

    def getSections(self):
        parser = self.read()
        return parser.sections()
