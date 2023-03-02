import os
import torch
import sounddevice as sd
import soundfile as sf
import hashlib


class TTSTacotron:
    def __init__(self, lang):
        self.model = self.model_init(lang=lang)

    def model_init(self, lang):
        model_url = {
            'ru': 'https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
            'de': 'https://models.silero.ai/models/tts/de/v3_de.pt'
        }
        if lang in model_url:
            url = model_url[lang]
        else:
            raise ValueError("Don't find language ", lang)
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = 'moduls/model_' + lang + '.pt'
        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file(url,local_file)
        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        model.to(device)
        return model
    def tell(self,text:str, pre_wav = None, speaker = 'kseniya'):
        if not text.strip():
            print("нечего говорить")
            return
        sample_rate = 48000
        #speaker = ru : ('aidar', 'baya', 'kseniya',
        #           'xenia', 'eugene', 'random')
        #speaker = de : (bernd_ungerer, eva_k, friedrich, hokuspokus, karlsson, random)
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