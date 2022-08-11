#
# объект класса Message служит контейнером сообщений для событий event


class Message:
    def __init__(self):
        self._text = ''
        self._command = ''
        self._message_sender = ''
        self._file_name = ''
        self._keyword = ''

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if isinstance(value, str):
            self._text = value
        else:
            raise(ValueError("Message.text must be a string"))

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
            raise (ValueError("Message.text must be a string"))

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        if isinstance(value, str):
            self._keyword = value
        else:
            raise (ValueError("Message.text must be a string"))

    def __call__(self):
        return (self.text, self.command, self.sender, self.file_name, self.keyword)