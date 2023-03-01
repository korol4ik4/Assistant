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
        self.tts = TTSTacotron()
        self.listen_from('NAME',text='*')
        self.listen_from('STT',info = '*')  # _ -когда есть info,
        self.talk_to('STT', command = '*')
        self.txt_to_speech=""

    def exe_command(self, message):
        #self.logger.debug(message.text)
        if "text" in message():
            if len(message.text) > 1:
                self.txt_to_speech = message.text
                self.post_message(command="mute")
        if "info" in message() and message.info == "mic_muted":
            if self.txt_to_speech:
                self.logger.debug(self.txt_to_speech)
                #kseniya, aidar, baya, xenia, eugene, random
                self.tts.tell(self.txt_to_speech, speaker = "xenia")
                self.post_message(command="mute_off")
                self.txt_to_speech =""

        ''' if message.text:
            msg = message
            pfile = msg.file_name
            fn = self.tts.tell_to_file(message.text, path_to_file="wav_cache/")
            if fn:
                msg.file_name = fn
            else:
                return
            if pfile and msg.command == "pre_wav":
                self.say(message)
            self.say(msg)
            if pfile and msg.command == "post_wav":
                self.say(message)
            '''