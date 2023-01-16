# coding:utf-8
"""
配置读取
"""
import yaml
import warnings
from shortcut_tools.common.set_path import CONFIG_FILE


def get_config():
    warnings.simplefilter('ignore', ResourceWarning)
    file = open(CONFIG_FILE, "r", encoding='utf-8')
    data = yaml.load(file.read(), Loader=yaml.Loader)
    return data
