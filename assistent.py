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
        log_level = logging.INFO  # DEBUG
        self.logger = get_base_logger(log_file_name, logger_name, log_level)
        #self.init_plugins(path="plugin")  # имя директории с файлами плагинов
        self.started = False
        self.paused = False

    def loop_stop(self):
        self.started = False
        self.paused = False

    def loop_start(self):
        if self.started:
            if self.paused:
                self.paused = False
            return  # снимаем с паузы
        if len(self.all_plugins):
            for name, plug in self.all_plugins.items():
                plug.close()
        self.all_plugins = {}
        self.init_plugins(path="plugin")  # имя директории с файлами плагинов
        self.loop()

    def on_event(self, new_event):
        pass

    def on_task(self,plugin_name,msg):
        pass

    def loop(self):
        self.logger.info("Дерево команд %s", Plugin.task())
        self.started = True
        try:
            while self.started:
                # Plugin.event = Событие - переменная класса, общая для всех потомков (плагинов)
                while self.paused:
                    pass
                new_event = Plugin.event.get()
                if new_event:
                    self.on_event(new_event)
                    self.logger.debug(" : Новое событие %s",  new_event())
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
                        message(search=keywords)
                        self.on_task(self.all_plugins[class_name].name, message)
                        exe_func(message)
                    else:
                        continue
        except BaseException() as e:  # KeyboardInterrupt:
            print(self.started, e)
        # выгрузить plugins (например завершить thread vosk  )
        self.logger.info("ВЫХОД!")
        for name, plug in self.all_plugins.items():
            plug.close()

    def import_plugins_from_path(self, path):
        try:
            files_in_dir = os.listdir(path)  # Получаем список файлов в dir
        except:
            print('ничего не найдено')
            return
        sys.path.insert(0, path)
        imported_plugins = []
        for s in files_in_dir:
            plugin_name = os.path.splitext(s)[0]
            if s.startswith("plugin") and s.endswith(".py"):
                self.logger.info('Найден Плагин %s ', plugin_name)
                print('Found plugin', plugin_name)
                imported_plugins.append(plugin_name)
                __import__(plugin_name, None, None, [''])  # Импортируем исходник плагина
        return imported_plugins

    def close_plugin(self, *plugin_names):
        for plugin_name in plugin_names:
            #print(plugin_name, self.all_plugins.keys())
            if plugin_name in self.all_plugins.keys():
                self.all_plugins[plugin_name].close()
                del self.all_plugins[plugin_name]

    def init_plugins(self, path):
        self.import_plugins_from_path(path)
        self.load_plugins()

    def load_plugins(self, *args):
        all = True if not args else False  # нет аргументов - загрузить все доступные плагины

        # так как Plugin произведен от object, мы используем __subclasses__,
        # чтобы найти все плагины, произведенные от этого класса
        for plugin in Plugin.__subclasses__():

            loaded = plugin.name in self.all_plugins
            if not loaded and (all or plugin.name in args):
                p = plugin()  # Создаем экземпляр класса из plugin_*
                self.all_plugins.update({p.name: p})  # имя плагина и он сам в словарь
                self.logger.info('Загружен %s', p.__class__)
                # print("Loaded ", p.__class__)

    @staticmethod
    def event_analyse(message_event):
        event = message_event()
        if 'sender' in event:
            event_type = event['sender']  # event список из event_type = имя плагина создавшего событие - text
        else:  # нет имени отправителя
            return

        tasks = Plugin.task()  # Plugin.task = Задания - переменная класса, общая для всех потомков (плагинов)
        pre_task = tasks.get(event_type)  # ветка заданий по заданному типу
        if pre_task:  # если есть такая ветка
            to_execute = []
            for act_task, keyword in pre_task.items():
                for tl, kw in keyword.items():
                    if tl in event:
                        data = event[tl]
                        result = keyword_search(data, kw)
                        if result:
                            pos = data.find(result[0])  # поиск позиции первого найденного слова
                            to_execute.append([pos, act_task, result, message_event])  # функция и данные для ее запуска
            if to_execute:
                # сортировка
                exe_order = sorted(to_execute, key=lambda x: x[0])  # сортировка по pos
                exe_order = [[fn, sres, msg] for pos, fn, sres, msg in exe_order]
                return exe_order
