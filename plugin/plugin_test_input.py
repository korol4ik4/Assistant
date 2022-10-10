#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from plugin import Plugin
import logging
from threading import Thread
import datetime


class TestInputPlugin(Plugin):
    name = "TEST_INPUT"  # необходимо переопределить в каждом плагине
    # default_options = {}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    def __init__(self):
        super(TestInputPlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.TerminalInput")
        self.thr = None
        self.started = True
        self.start_()
        self.talk_to('INPUT', keyword="*")  # подписать plugin to_name на события от текущего plugin self.name
        # self.listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию
    def input_loop(self):
        n = 0
        start_at = datetime.datetime.now()
        try:
            while self.started:
                if not self.started:
                    raise KeyboardInterrupt()
                if n==100_000:
                    print(start_at)
                    raise KeyboardInterrupt()

                # self.say(text_input)
                self.post_message(text=str(n) + " " + str(datetime.datetime.now()), title = "time")
                n+=1
        except KeyboardInterrupt:
            # выгрузить plugins (например завершить thread vosk  )
            self.logger.debug("input loop break")

    def start_(self):
        self.thr = Thread(target=self.input_loop)
        self.thr.start()

    def close(self):
        self.started = False
        if self.thr:
            self.logger.info("close signal")
            # pyautogui.press('enter')
            print("press Enter to Exit")
            self.thr.join()
