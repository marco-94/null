# coding:utf-8
"""
路径配置
"""
import os, sys
from shortcut_tools.common import yaml_reader

# BASE_PATH = os.getcwd()
# sys.path.append(BASE_PATH)
# CONFIG_FILE = os.path.join(BASE_PATH, 'file', 'config.yml')
CONFIG_FILE = 'D://test//null//shortcut_tools//file//config.yml'


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = yaml_reader.YamlReader(config).data

    def get(self, element, index=0):
        return self.config[index].get(element)
