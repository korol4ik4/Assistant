#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from plugin import Plugin
import logging
from message import Message
import datetime

class ChangeLanguagePlugin(Plugin):
    name = "LANGUAGE"  # необходимо переопределить в каждом плагине
      # можно переопределить для сохранения/ручного редактирования и загрузки настроек
    def __init__(self):
        super(ChangeLanguagePlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.Language")
        # подписать plugin to_name на события от текущего plugin self.name
        self.listen_from('NAME', text = '*мени язык*|sprach* *ände*|chang* lang*')
        self.talk_to('STT', command='language_*')

        # self.listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию

    def exe_command(self, message):
        #self.logger.debug(" : %s", message() )
        if 'text' in message():

        if "lang" in message():
            if message.lang == 'ru':
                self.post_message(command='language_de')
            else:
                self.post_message(command = 'language_ru')

