#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from plugin import Plugin
import logging
from message import Message
import datetime

class NamePlugin(Plugin):
    name = "NAME"  # необходимо переопределить в каждом плагине
    name_ru = "ассистент"
    name_de = "assistent"
    name_en = "assistant"
    _or = '|'
    all_name = name_en + _or + name_de + _or + name_ru
    default_options = {"name": all_name}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    def __init__(self):
        super(NamePlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.Name")
        # подписать plugin to_name на события от текущего plugin self.name
        if "name" in self.options:
            name = self.options["name"]
        else:
            self.logger.info("don't find name for Assistent, name = 'ассистент'")
            name = "ассистент"
        self.listen_from('STT', text = name)
        # text='*'
        # self.listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию

    def exe_command(self, message):
        #self.logger.debug(" : %s", message() )
        if "text" in message() and "search" in message():
            msg = Message(**message())
            text = message.text
            for s in message.search:
                text = text.replace(s, "")
            del msg.search
            msg.text=text
            self.post_message(msg)
