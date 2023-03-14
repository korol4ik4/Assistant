from plugin import Plugin
from moduls.tts_silero import TTSTacotron
from message import Message
import logging


class TextToSpeechPlugin(Plugin):
    name = "TTS"  # уникальное имя плагина

    def __init__(self):
        super(TextToSpeechPlugin, self).__init__()
        # Инициализация и запуск распознавания голоса
        self.logger = logging.getLogger("Assistant.Plugin.silero_tts")
        self.tts = None
        self.speaker = 'random'
        self.language = 'ru'
        self.set_lang(lang=self.language)
        self.listen_from('NAME')
        self.listen_from('STT',info = 'mic*')  # _ -когда есть info,
        self.talk_to('STT', command = 'o??_mute') # посылать команды вкл./откл. микрофон
        self.txt_to_speech=""

    def set_lang(self,lang):
        self.tts = TTSTacotron(lang=lang)
        self.language = lang
        if lang == 'ru':
            self.speaker = "xenia"
        elif lang == 'de':
            self.speaker = "eva_k"
        elif lang == 'en':
            self.speaker = "en_85"

    def exe_command(self, message):
        #self.logger.debug(message.text)
        if "text" in message():
            if len(message.text) > 1:
                self.txt_to_speech = message.text
                #-------------------
                if 'lang' in message() and self.language != message.lang:
                    try:
                        self.set_lang(message.lang)
                        self.language = message.lang
                    except:
                        self.set_lang(self.language)
                self.post_message(command="on_mute")
        if "info" in message() and message.info == "mic_off":
            if self.txt_to_speech:
                self.logger.debug(self.txt_to_speech)
                #kseniya, aidar, baya, xenia, eugene, random
                self.tts.tell(self.txt_to_speech.lower(), speaker = self.speaker)
                self.post_message(command="off_mute")
                self.txt_to_speech =""