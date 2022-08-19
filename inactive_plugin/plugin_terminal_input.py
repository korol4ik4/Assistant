#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from message import Message
from plugin import Plugin
import logging
from threading import Thread


class TerminalInputPlugin(Plugin):
    name = "TERMINAL_INPUT"  # необходимо переопределить в каждом плагине
    # default_options = {}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    def __init__(self):
        super(TerminalInputPlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.TerminalInput")
        self.thr = None
        self.started = True
        self.start_terminal()


        self.talk_to('INPUT', keyword="*") # подписать plugin to_name на события от текущего plugin self.name
        # self.listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию
    def input_loop(self):
        tinput = ''
        msg = Message()
        msg.sender = self.name
        try:
            while self.started:
                self.logger.debug("command : %s", tinput)
                tinput = input('введи комманду \n')
                if not self.started:
                    raise KeyboardInterrupt()
                if tinput:
                    msg.text = tinput
                else:
                    msg.text = ''
                if msg.text:
                    self.say(msg)

        except KeyboardInterrupt as e:
            # выгрузить plugins (например завершить thread vosk  )
            self.logger.debug("ВЫХОД")


    def start_terminal(self):
        self.thr = Thread(target=self.input_loop)
        self.thr.start()

    def close(self):
        self.started = False
        if self.thr:
            self.thr.join()
            self.thr = None

