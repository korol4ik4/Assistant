#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from plugin import Plugin
import logging


class TerminalOutputPlugin(Plugin):
    name = "TERMINAL_OUTPUT"  # необходимо переопределить в каждом плагине
    # default_options = {}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    def __init__(self):
        super(TerminalOutputPlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.TerminalOutput")
        # подписать plugin to_name на события от текущего plugin self.name
        self.listen_from('TERMINAL_INPUT', keyword="")
        # self.listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию

    def exe_command(self, message):
        self.logger.debug(" : %s", message)
