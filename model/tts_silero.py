import os
import torch
import sounddevice as sd
import soundfile as sf


class TTSTacotron:
    def __init__(self):
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = 'plugin_src/model_ru.pt'
        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                           local_file)
        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        model.to(device)
        self.model = model


    def tell(self,text:str, pre_wav = None, speaker = 'kseniya'):
        if not text.strip():
            print("нечего говорить")
            return
        sample_rate = 48000
        #speaker = ['aidar', 'baya', 'kseniya',
        #           'xenia', 'eugene', 'random']
        put_accent = True
        put_yo = True

        audio = self.model.apply_tts(text=text,
                                speaker=speaker,
                                sample_rate=sample_rate,
                                put_accent=put_accent,
                                put_yo=put_yo)
        if pre_wav:
            data, fs = sf.read(pre_wav, dtype='float32')
            sd.play(data, fs)
            sd.wait()
        sd.play(audio, samplerate=sample_rate)
        sd.wait()

'''
t = TacotronTTS()
t.tell('привет виталик')
'''