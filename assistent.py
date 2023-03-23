#
# Assistant class
from threading import Thread
from base_logger import get_base_logger
import logging
import sys
import os
from plugin import Plugin
from message import Message

from utils.parser import keyword_search


class Assistant(object):

    def __init__(self):
        self.all_plugins = {}  # словарь {str - имя плагина: object - инициализированный плагин}
        log_file_name = "assistant.log"
        logger_name = "Assistant"
        log_level = logging.DEBUG  # INFO
        self.logger = get_base_logger(log_file_name, logger_name, log_level)
        #self.init_plugins(path="plugin")  # имя директории с файлами плагинов
        self.started = False
        self.paused = False
        self._list_event = False
        self._event_sender = []
        self._list_task = False
        self._task_actor = []
        self.thr_loop = None

    # --------------------------------------------
    @staticmethod
    def event_add(message: dict):
        msg = Message(**message)
        return Plugin.event.add(msg)

    def event_list(self,*args):
        self._event_sender = []
        if args:
            if args[0] == 'all':
                self._list_event = True
            elif args[0] == 'nix':
                self._list_event = False
            else:  # names of Plugin
                # test: Plugin with name is loaded
                self._event_sender = [name for name in args if name in self.all_plugins.keys()]
                if self._event_sender:
                    self._list_event = True
        else:
            self._list_event = True  # default 'all'

        if not self._list_event:
            return "not listen events"
        if self._event_sender:
            return f'listen events from {self._event_sender}'
        else:
            return 'listen all events'
    # --------------------------------------------

    @staticmethod
    def task_add(sender, acceptor, **kwargs):
        if not kwargs:
            kwargs = {'text': '*'}
        new_task = {sender: {acceptor: kwargs}}
        return Plugin.task.update(new_task)

    def task_list(self, *args):
        if len(args) == 0:
            return Plugin.task()
        elif len(args) == 1:
            if args[0] == 'all':
                self._task_actor = []
                self._list_task = True
            elif args[0] == 'nix':
                self._list_task = False
            elif args[0] in self.all_plugins.keys():
                self._task_actor.append(args[0])
                self._list_task = True
        else:
            self._task_actor = [name for name in args if name in self.all_plugins.keys()]
            if self._task_actor:
                self._list_task = True

        if not self._list_task:
            return "not listen tasks"
        if self._task_actor:
            return f'listen tasks for {self._task_actor}'
        else:
            return 'listen all tasks'

    @staticmethod
    def task_del(*args):
        sender = None
        acceptor = None
        field_name = []
        if len(args) == 1:
            sender = args[0]
        elif len(args) > 1:
            sender, acceptor, *field_name = args
            #field_name = [] if not field_name else field_name[0]

        if sender == 'all':
            Plugin.task._all_task = {}
            return True
        else:
            return Plugin.task.delete(sender, acceptor, *field_name)
    # --------------------------------------------

    def on_event(self, new_event):
        pass

    def on_task(self,plugin_name,msg):
        pass
    # --------------------------------------------

    def loop_start(self):
        self.paused = False
        if self.started:
            return 'Assistant loop already been launched'
        if not self.thr_loop:  # защита от двойного запуска
            self.thr_loop = Thread(target=self.loop, name="Assistant_Main_Loop")
            self.thr_loop.start()
        else:
            self.thr_loop.join()
            return 'Assistant loop start problem..'
        return 'Assistant loop started'

    def loop_stop(self):
        self.started = False
        self.paused = False
        self.thr_loop.join()
        self.thr_loop = None
        return 'Assistant loop stopped'

    def loop_pause(self):
        self.paused = True
        return 'Assistant loop paused'

    def loop_stat(self):
        if not self.started:
            return 'Assistant loop stopped'
        else:
            if self.paused:
                return 'Assistant loop paused'
            else:
                return 'Assistant loop launched'
    # --------------------------------------------

    def plugin_list(self, *args):
        import_plugs = [pl.name for pl in Plugin.__subclasses__()]
        load_plugs = list(self.all_plugins.keys())
        if len(args) == 0:  # default all
            return f"imported Plugins: {import_plugs}\nloaded Plugins: {load_plugs}"
        if len(args) == 1:
            if args[0] == 'all':  # all
                return f"imported Plugins: {import_plugs}\nloaded Plugins: {load_plugs}"
            elif args[0] == 'loaded':
                return f"loaded Plugins: {load_plugs}"
            elif args[0] == 'imported':
                return f"imported Plugins: {import_plugs}"
        return f"can't parse {args}"

    def import_plugins_from_path(self, path):
        try:
            files_in_dir = os.listdir(path)  # Получаем список файлов в dir
        except:
            # print('ничего не найдено')
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

    def load_plugins(self, *plugin_names):
        if not plugin_names or plugin_names[0] == 'all':
            load_all = True  # нет аргументов - загрузить все доступные плагины
        else:
            load_all = False
        # так как Plugin произведен от object, мы используем __subclasses__,
        # чтобы найти все плагины, произведенные от этого класса
        for plugin in Plugin.__subclasses__():
            loaded = plugin.name in self.all_plugins
            if not loaded and (load_all or plugin.name in plugin_names):
                p = plugin()  # Создаем экземпляр класса из plugin_*
                self.all_plugins.update({p.name: p})  # имя плагина и он сам в словарь
                self.logger.info('Загружен %s', p.__class__)
        return list(self.all_plugins.keys())

    def close_plugin(self, *plugin_names):
        if plugin_names and plugin_names[0] == 'all':
            for plug in self.all_plugins.values():
                plug.close()
            self.all_plugins = {}
            return "all plugins closed"
        ret = []
        for plugin_name in plugin_names:
            # print(plugin_name, self.all_plugins.keys())
            if plugin_name in self.all_plugins.keys():
                self.all_plugins[plugin_name].close()
                del self.all_plugins[plugin_name]
                ret.append(plugin_name)
        return ret
    def init_plugins(self, path='plugin'):
        self.import_plugins_from_path(path)
        self.load_plugins()
    # --------------------------------------------

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
        self.started = False
        # выгрузить plugins (например завершить thread vosk  )
        self.logger.info("ВЫХОД!")
        for name, plug in self.all_plugins.items():
            plug.close()


