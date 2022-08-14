#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from message import Message
from plugin import Plugin
import logging

class ConsoleInputPlugin(Plugin):
    name = "INPUT"  # необходимо переопределить в каждом плагине
    default_options = {}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    def __init__(self):
        super(ConsoleInputPlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.Input")
        self.exe_command(Message())
        self.talk_to('INPUT', keyword="*") # подписать plugin to_name на события от текущего plugin self.name
    #listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию

    def exe_command(self, message):
        self.logger.debug("message : %s", message())
        if 'stop' in message.keyword:
            raise KeyboardInterrupt('Выход')
        msg = Message()
        msg.text = input('введи команду ')
        msg.sender = self.name
        msg.command = 'быстро'
        msg.file_name = 'wav/82452ß9582ß9dj329.wav'
        self.say(msg)
        # start_string = self.options['start_string'] #получение настроек
        # ваш код
        # ваш код
        # ваш код
        # создать событие после завершения
        # self.say(message)
        # подписаться на событие
        # return self.return_task(task_type, keyword)
        # завладеть вниманием