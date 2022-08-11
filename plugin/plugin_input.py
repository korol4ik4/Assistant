#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from message import Message
from plugin import Plugin


class ConsoleInputPlugin(Plugin):
    name = "INPUT"  # необходимо переопределить в каждом плагине
    default_options = {}  # можно переопределить для сохранения/ручного редактирования и загрузки настроек

    def __init__(self):
        super(ConsoleInputPlugin, self).__init__()
        msg = Message()
        msg.sender = self.name
        self.say(msg)
        print(msg)
    #talk_to(self, to_name, keyword="*") # подписать plugin to_name на события от текущего plugin self.name
    #listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию

    def input_command(self):
        while True:
            msg = Message()
            msg.text = input('введи команду')
            msg.sender = self.name
            self.say(msg)

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