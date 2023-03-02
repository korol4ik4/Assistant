#
# Plugin SpeechToText
from plugin import Plugin
from moduls.stt_vosk import SpeechToText
import logging


class SpeechToTextPlugin(Plugin):
    name = "STT"  # уникальное имя плагина

    def __init__(self):
        super(SpeechToTextPlugin, self).__init__()
        # Инициализация и запуск распознавания голоса
        self.logger = logging.getLogger("Assistant.Plugin.VoskSTTInput")
        self.stt = None
        self.set_lang(lang='ru')#lang


    def set_lang(self, lang):
        if self.stt:
            self.close()
        self.stt = SpeechToText(lang=lang)
        self.stt.bind(self.voice_input)
        # self.talk_to('INPUT', keyword="*")  # подписать plugin to_name на события от текущего plugin self.name
        self.stt.start()

    def voice_input(self, txt, *args):  # исполняется когда stt-vosk распознал предложение
        '''
        msg = Message()
        msg.text = txt
        if args:
            if args[0] == "LocMic" or args[0] == "LocFile":
                msg.sender = self.name
            else:
                msg.sender = args[0]

        # Логирование если нужно
        # logger = logging.getLogger(self.logger.name + " " + self.name + " voice_input_function")
        # logger.debug("Распознано: '%s'", txt)
'''
        return self.post_message(text=txt,args=args)  # добавляет распознанный текст в события. event = ("STT", txt)

    def exe_command(self, message):
        cmd = ""
        if "command" in message():
            cmd = message.command
        # отключить / включить распознавание, начать / остановить запись с микрофона (пока RAW данные)
        if cmd == "mute":

            #self.stt.stop()
            self.stt.mute_on()
            self.post_message(info = "mic_off")

        elif cmd == "mute_off":
            #self.stt.start()
            self.stt.mute_off()
            self.post_message(info="mic_on")

        elif "record_wav" in cmd:
            if message.file_name:
                self.stt.rec_wav(message.file_name)
        elif "record_wav_stop" in cmd:
            self.stt.rec_wav_stop()

        elif "recognize_from_file" in cmd:
            if message.file_name:
                self.stt.from_file(message.file_name, message.sender)

    def close(self):  # выйти из бесконечного цикла (внутри модуля stt_vosk) перед закрытием программы / плагина
        if self.stt:
            self.stt.stop()
            self.logger.info("Выход")
            self.stt = None

