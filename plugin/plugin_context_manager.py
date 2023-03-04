#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from plugin import Plugin
import logging
from message import Message
import datetime

class ContextPlugin(Plugin):
    name = "CONTEXT"  # необходимо переопределить в каждом плагине
    default_options = {}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    def __init__(self):
        super(ContextPlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.Context")
        # подписать plugin to_name на события от текущего plugin self.name
        self.listen_from('STT')# text='*'
        self.on_context = False
        # self.listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию

    def exe_command(self, message):
        #self.logger.debug(" : %s", message() )
        if "command" in message():
            if message.command == "on_context":
                self.on_context = True

        if self.on_context:
            if "text" in message() and "sender" in message():
                if message.sender == 'STT':
                    msg = Message(**message())
                    msg(context = msg.text)
                    del msg.text
                    self.post_message(msg)
                    self.on_context = False
