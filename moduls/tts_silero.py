import os
import torch
import sounddevice as sd
import soundfile as sf
import hashlib


class TTSTacotron:
    def __init__(self):
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = 'model/model_ru.pt'
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

    def tell_to_file(self, text, path_to_file = '', speaker = 'kseniya'):
        _hash = hashlib.md5()  # sha3_256()
        _hash.update(text.encode())
        file_name = str(_hash.hexdigest()) + '.wav'
        files_in_dir = os.listdir(path_to_file)
        if file_name in files_in_dir:
            return path_to_file + file_name
        sample_rate = 48000
        try:
            audio_paths = self.model.save_wav(text=text,
                                         speaker=speaker,
                                         sample_rate=sample_rate,
                                         audio_path=path_to_file + file_name)
        except ValueError:
            # print("служебное сообщение")
            audio_paths = None

        return audio_paths
'''
t = TacotronTTS()
t.tell('привет виталик')
'''