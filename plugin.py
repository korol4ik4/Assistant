#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from json_options import Options
from event import Event
from task import Task
from message import Message

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
            self.options = Options(self.__class__.__name__, self.default_options, path="plugin_options").get()

    def talk_to(self, to_name, **keyword):  # подписать plugin to_name на события от текущего plugin self.name
        if len(keyword) < 1:
            keyword = {'text': '*'}
        task = {self.name: {
            to_name : keyword
        }}
        self.task.update(task)

    def listen_from(self, from_name, **keyword):  # подписаться на события от plugin from_name
        if len(keyword) < 1:
            keyword = {'text': '*'}  # default
        task = {from_name: {
            self.name : keyword
        }}
        self.task.update(task)

    def not_listen_from(self, sender, *felds):
        self.task.delete(sender,self.name, felds)

    def not_talk_to(self, acceptor, *felds):
        self.task.delete(self.name,acceptor, felds)

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию
    def exe_command(self, message):
        pass
        # start_string = self.options['start_string'] #получение настроек
        # ваш код
        # ваш код
        # ваш код
        # создать событие после завершения
        # self.say(message)
        # подписаться на событие
        # return self.return_task(task_type, keyword)
        # завладеть вниманием

    def post_message(self, *args, **kwargs):
        message = Message(sender=self.name, chain=[self.name])
        if len(args):
            if isinstance(args[0], Message):  # Если есть аргумент и он является Message
                message = args[0]
                if 'chain' in message():
                    chain = message.chain
                else:
                    chain = ['NOBODY',]
                if isinstance(chain,list):
                    chain.append(self.name)
                else:
                    chain = [chain,self.name]
                message(sender=self.name, chain = chain)  # меняем имя отправителя и добавляем его в цепочке
        message(** kwargs)  # добавляем именованные аргументы в сообщение
        event = message
        # print(event)
        self.event.add(event)  # создаём событие (отправка сообщения)

    def close(self):
        # завершить если необходимо
        pass
