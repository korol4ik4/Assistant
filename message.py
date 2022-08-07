#
# объект класса Message служит контейнером сообщений для событий event


class Message:
    def __init__(self):
        self._text = ''
        self._command = ''
        self._message_sender = ''
        self._file_name = ''

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def command(self):
        return self._command

    @text.setter
    def command(self, value):
        self._command = value

    @property
    def sender(self):
        return self._message_sender

    @text.setter
    def sender(self, value):
        self._message_sender = value

    @property
    def file_name(self):
        return self._file_name

    @text.setter
    def file_name(self, value):
        self._file_name = value
