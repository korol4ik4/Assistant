#
# Assistant class

from base_logger import get_base_logger
import logging
import sys
import os
from plugin import Plugin


class Assistant(object):

    def __init__(self):
        self.all_plugins = {}  # словарь {str - имя плагина: object - инициализированный плагин}
        log_file_name = "assistant.log"
        logger_name = "Assistant"
        log_level = logging.DEBUG
        self.logger = get_base_logger(log_file_name, logger_name, log_level)
        self.load_plugins(path="plugin")  # имя директории с файлами плагинов

    def loop(self):
        pass

    def load_plugins(self, path):
        files_in_dir = os.listdir(path)  # Получаем список файлов в dir
        sys.path.insert(0, path)  # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить

        for s in files_in_dir:
            plugin_name = os.path.splitext(s)[0]
            if s.startswith("plugin") and s.endswith(".py"):
                self.logger.info('Найден Плагин %s', s)
                # print('Found plugin', s)
                __import__(plugin_name, None, None, [''])  # Импортируем исходник плагина
        # так как Plugin произведен от object, мы используем __subclasses__,
        # чтобы найти все плагины, произведенные от этого класса
        for plugin in Plugin.__subclasses__():
            if plugin.name not in self.all_plugins:
                p = plugin()  # Создаем экземпляр класса из plugin_*
                self.all_plugins.update({p.name: p})  # имя плагина и он сам в словарь
                self.logger.info('Загружен %s', p.__class__)
                # print("Loaded ", p.__class__)
