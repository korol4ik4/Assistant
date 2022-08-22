from plugin import Plugin
from message import Message
import logging
import sounddevice as sd
import soundfile as sf


class VoiceOutputPlugin(Plugin):
    name = "VOICE"  # уникальное имя плагина

    def __init__(self):
        super(VoiceOutputPlugin, self).__init__()
        # Инициализация и запуск распознавания голоса
        self.logger = logging.getLogger("Assistant.Plugin.voice_output")
        self.listen_from('TTS')
        self.queue = []
        self.listen_from('STT')
        self.talk_to('STT')

    def exe_command(self, message):
        msg_on = Message()
        msg_on.command = "mute_on"
        msg_off = Message()
        msg_off.command = "mute_off"

        if message.command == "mic_muted":
            if self.queue:
                for file in self.queue:
                    self.play_wav(message.file_name)
                self.queue = []
                self.say(msg_off)
        elif message.file_name:
            self.queue.append(message.file_name)
            self.say(msg_on)

    @staticmethod
    def play_wav(file_name):
        data, fs = sf.read(file_name, dtype='float32')
        sd.play(data, fs)
        sd.wait()
