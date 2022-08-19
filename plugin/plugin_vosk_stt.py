#
# Plugin SpeechToText
from plugin import Plugin
from model.stt_vosk import SpeechToText
from message import Message
import logging


class SpeechToTextPlugin(Plugin):
    name = "STT"  # уникальное имя плагина

    def __init__(self):
        super(SpeechToTextPlugin, self).__init__()
        # Инициализация и запуск распознавания голоса
        self.logger = logging.getLogger("Assistant.Plugin.VoskSTTInput")
        self.stt = SpeechToText()
        self.stt.bind(self.voice_input)
        self.talk_to('INPUT', keyword="*")  # подписать plugin to_name на события от текущего plugin self.name
        self.stt.start()

    def voice_input(self, txt, *args):  # исполняется когда stt-vosk распознал предложение
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

        return self.say(msg)  # добавляет распознанный текст в события. event = ("STT", txt)

    def on_command(self, msg):
        cmd = msg.command
        # print(cmd)
        # отключить / включить распознавание, начать / остановить запись с микрофона (пока RAW данные)
        if "mute_on" in cmd:
            msg = Message()
            msg.text = "mic_muted"
            #self.stt.stop()
            self.stt.mute_on()
            self.say(msg)
        elif "mute_off" in cmd:
            #self.stt.start()
            self.stt.mute_off()

        elif "record_vaw" in cmd:
            if msg.file_name:
                self.stt.rec_wav(msg.file_name)
        elif "record_vaw_stop" in cmd:
            self.stt.rec_wav_stop()

        elif "recognize_from_file" in cmd:
            if msg.file_name:
                self.stt.from_file(msg.file_name, msg.sender)

    def close(self):  # выйти из бесконечного цикла (внутри модуля stt_vosk) перед закрытием программы / плагина
        self.stt.stop()
        self.logger.info("Выход")

