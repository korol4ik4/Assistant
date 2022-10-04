#
# Assistant class

from base_logger import get_base_logger
import logging
import sys
import os
from plugin import Plugin
from utils.parser import keyword_search


class Assistant(object):

    def __init__(self):
        self.all_plugins = {}  # словарь {str - имя плагина: object - инициализированный плагин}
        log_file_name = "assistant.log"
        logger_name = "Assistant"
        log_level = logging.DEBUG
        self.logger = get_base_logger(log_file_name, logger_name, log_level)
        self.load_plugins(path="plugin")  # имя директории с файлами плагинов

    def loop(self):
        self.logger.info("Дерево команд %s", Plugin.task().items())
        try:
            while True:
                # Plugin.event = Событие - переменная класса, общая для всех потомков (плагинов)
                new_event = Plugin.event.get()
                if new_event:
                    send = new_event['message_sender']
                    msg = new_event['text']
                    self.logger.debug("Новое событие %s, %s", send, msg)
                    # print('##event## ', new_event)
                    # print('%%TasksBaum%% ', Plugin.task())
                    new_tasks = self.event_analyse(new_event)
                else:
                    continue
                if not new_tasks:
                    continue
                # есть что- то к исполнению
                for class_name, keywords, message in new_tasks:
                    if class_name in self.all_plugins:
                        exe_func = self.all_plugins[class_name].exe_command
                        exe_func(message)
                    else:
                        continue
        except KeyboardInterrupt:
            # выгрузить plugins (например завершить thread vosk  )
            self.logger.info("ВЫХОД")
            for name, plug in self.all_plugins.items():
                plug.close()

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

    @staticmethod
    def event_analyse(event):
        event_type = event['message_sender']  # event список из event_type = имя плагина создавшего событие - text
        text = event['text']
        tasks = Plugin.task()  # Plugin.task = Задания - переменная класса, общая для всех потомков (плагинов)
        pre_task = tasks.get(event_type)  # ветка заданий по заданному типу
        if pre_task:  # если есть такая ветка
            to_execute = []
            for keyword in pre_task.keys():  # ключевые слова из ветки заданий
                result = keyword_search(text, keyword)  # список найденных слова целиком
                if result:  # ключевые слова найдены
                    pos = text.find(result[0])  # поиск позиции первого найденного слова
                    act_task = pre_task[keyword]  # принимающая функция / функции
                    for a_task in act_task.split(","):
                        to_execute.append([pos, a_task, result, event])  # функция и данные для ее запуска
            if to_execute:
                # сортировка
                exe_order = sorted(to_execute, key=lambda x: x[0])  # сортировка по pos
                exe_order = [[fn, sres, msg] for pos, fn, sres, msg in exe_order]
                return exe_order
