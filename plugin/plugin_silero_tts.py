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
