#
# объект класса Message служит контейнером сообщений для событий event


class Message:
    def __init__(self, text = '', command = '', message_sender = '', file_name = '', keyword = ''):
        self._text = text
        self._command = command
        self._message_sender = message_sender
        self._file_name = file_name
        self._keyword = keyword

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        if isinstance(value, str):
            self._command = value
        else:
            raise (ValueError("Message.text must be a string"))

    @property
    def sender(self):
        return self._message_sender

    @sender.setter
    def sender(self, value):
        if isinstance(value, str):
            self._message_sender = value
        else:
            raise (ValueError("Message.text must be a string"))

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if isinstance(value, str):
            self._file_name = value
        else:
            raise (ValueError("Message.file_name must be a string"))

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        if isinstance(value, list):
            self._keyword = value
        else:
            raise (ValueError("Message.keyword must be a list %s", value))

    def __call__(self):
        return self.text, self.command, self.sender, self.file_name, self.keyword

#
# объект класса Message служит контейнером сообщений для событий event
# Message использовать JSON? - создаём стандартный словарь:
# Message = {{
#               'text' : '',
#               'command : '',
#               'message_sender' : '',
#               'file_name' : None  # null
#               'keywords' : ''
#               'port_in' : None
#               'port_out' : None
#           }}
# Обрезаем все не нужное с возможностью расширения
# Message = {
#               'message_sender' : '',
#               'text' : ''
#           }
