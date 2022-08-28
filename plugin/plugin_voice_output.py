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
        self.listen_from('STT',keyword="_command_")
        self.talk_to('STT',keyword="_command_")
        self.queue = []
        self.msg_mic_on = Message(text= "_command_", command="mute_off")
        self.msg_mic_off = Message(text="_command_", command="mute_on")

    def exe_command(self, message):
        if message.file_name:
            self.queue.append(message)
            self.say(self.msg_mic_off)
        elif message.command == "mic_muted":
            for msg in self.queue:
                self.logger.info("Говорит: %s", msg.text)
                self.play_wav(msg.file_name)
            self.queue = []
            self.say(self.msg_mic_on)

    @staticmethod
    def play_wav(file_name):
        data, fs = sf.read(file_name)
        sd.play(data, fs)
        sd.wait()
