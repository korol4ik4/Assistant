#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from json_options import Options
from event import Event
from task import Task

import logging


class Plugin(object):
    name = "undefined"  # необходимо переопределить в каждом плагине
    default_options = {}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    event = Event()  # события
    task = Task()  # задачи

    def __init__(self):
        self.logger = logging.getLogger("Assistant.Plugin")
        if self.default_options:
            # загрузка настроек
            self.options = Options(self.name, self.default_options, path="plugin_options").get()

    def talk_to(self, to_name, keyword="*"):  # подписать plugin to_name на события от текущего plugin self.name
        task = {self.name: {
            keyword: to_name
        }}
        self.task.update(task)

    def listen_from(self, from_name, keyword="*"):  # подписаться на события от plugin from_name
        task = {from_name: {
            keyword: self.name
        }}
        self.task.update(task)

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию
    def on_command(self, *args):
        pass
        # start_string = self.options['start_string'] #получение настроек
        # ваш код
        # ваш код
        # ваш код
        # создать событие после завершения
        # self.say(data)
        # подписаться на событие
        # return self.return_task(task_type, keyword)
        # завладеть вниманием
        # return self.return_task_mute_other(task_type, keyword)

    def say(self, *data):  # возвращает событие
        event = self.name, data
        self.event.add(event)  # list(тип, данные)

    def close(self):
        # завершить если необходимо
        pass
