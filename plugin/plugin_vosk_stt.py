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
        self.language = 'ru'
        self.logger = logging.getLogger("Assistant.Plugin.VoskSTTInput")
        self.stt = None
        self.set_lang(lang=self.language)#lang


    def set_lang(self, lang):
        if self.stt:
            self.close()
        self.stt = SpeechToText(lang=lang)
        self.language = lang
        self.stt.bind(self.voice_input)
        #self.listen_from('NAME')
        # self.talk_to('INPUT', keyword="*")  # подписать plugin to_name на события от текущего plugin self.name
        self.stt.start()

    def voice_input(self, txt, *args):  # исполняется когда stt-vosk распознал предложение
        return self.post_message(text=txt,args=args,lang=self.language)  # добавляет распознанный текст в события. event = ("STT", txt)

    def exe_command(self, message):
        cmd = ""
        if "command" in message():
            cmd = message.command
        else:
            return
        # отключить / включить распознавание, начать / остановить запись с микрофона (пока RAW данные)
        if cmd == "on_mute":

            #self.stt.stop()
            self.stt.mute_on()
            self.post_message(info = "mic_off")

        elif cmd == "off_mute":
            #self.stt.start()
            self.stt.mute_off()
            self.post_message(info="mic_on")

        elif "on_record_wav" in cmd:
            if message.file_name:
                self.stt.rec_wav(message.file_name)
        elif "off_record_wav" in cmd:
            self.stt.rec_wav_stop()

        elif "from_file_recognize" in cmd:
            if message.file_name:
                self.stt.from_file(message.file_name, message.sender)
        elif "language_" in cmd:
            lang = cmd[len('language_'):]
            self.set_lang(lang)
            self.post_message(info= "language changed " + lang)

    def close(self):  # выйти из бесконечного цикла (внутри модуля stt_vosk) перед закрытием программы / плагина
        if self.stt:
            self.stt.stop()
            self.logger.info("Выход")
            self.stt = None

