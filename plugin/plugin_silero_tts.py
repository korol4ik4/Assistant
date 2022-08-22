from plugin import Plugin
from model.tts_silero import TTSTacotron
from message import Message
import logging


class TextToSpeechPlugin(Plugin):
    name = "TTS"  # уникальное имя плагина

    def __init__(self):
        super(TextToSpeechPlugin, self).__init__()
        # Инициализация и запуск распознавания голоса
        self.logger = logging.getLogger("Assistant.Plugin.silero_tts")
        self.tts = TTSTacotron()
        self.listen_from('STT')

    def exe_command(self, message):
        if message.text:
            msg = message
            pfile = msg.file_name
            msg.file_name = self.tts.tell_to_file(message.text, path_to_file="wav_cache/")
            if pfile and msg.command == "pre_wav":
                self.say(message)
            self.say(msg)
            if pfile and msg.command == "post_wav":
                self.say(message)
