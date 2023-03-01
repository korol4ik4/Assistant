import queue
import sounddevice as sd
import vosk
import sys
import json
from threading import Thread

from vosk import Model, KaldiRecognizer, SetLogLevel
import subprocess

class STTVosk:
    def __init__(self, lang="ru", device=None,
                 samplerate=16000):
        self.que = queue.Queue()
        self.device = device
        try:
            if samplerate is None:
                device_info = sd.query_devices(device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                self.samplerate = int(device_info['default_samplerate'])
            else:
                self.samplerate = samplerate
        except Exception as e:
            print('Device not correct ', device, str(e))

        self.samplerate = samplerate

        self.model = vosk.Model(lang=lang)
        self.rec = vosk.KaldiRecognizer(self.model, self.samplerate)
        self.dump_fn = None  # запись в фаил с микрофона
        self._mic_list = True
        self._off_recognize = False
        self.off_recognize = False
        # self.rec.SetWords(('дом','вася'))
        # self.model = vosk.Model("vosk-model-ru-0.22")

    def mute_on(self):
        self.off_recognize = True
        self._off_recognize = True

    def mute_off(self):
        self._off_recognize = False

    def mic_listen_stop(self):
        self._mic_list = False

    def rec_wav(self, filename):
        if filename:
            self.dump_fn = open(filename, "wb")
        else:
            self.dump_fn = None
        # self.listen_on = True

    def rec_wav_stop(self):
        if self.dump_fn:
            try:
                self.dump_fn.close()
            except:
                print(self.dump_fn, " wav file is incorrect closed ")
        self.dump_fn = None

    def mic_listen(self):
        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)

            #if not self._off_recognize:
            self.que.put(bytes(indata))

        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=self.device, dtype='int16',
                                   channels=1, callback=callback):

                self._mic_list = True
                while self._mic_list:
                    data = self.que.get()
                    # Запись в фаил
                    if self.dump_fn is not None:
                        self.dump_fn.write(data)
                    # выход из цикла (завершение)
                    if not self._mic_list:
                        break
                    # вкл. / выкл. распознования
                    if self.off_recognize:
                        if not self._off_recognize:
                            self.off_recognize = False
                        continue
                    # распознование
                    if self.rec.AcceptWaveform(data):
                        result = json.loads(self.rec.Result())["text"]
                        if result:
                            self.recognized(result,"local_mic")
                    else:
                        pass
                        # self.on_partial(self.rec.PartialResult()[17:-3])
                        # print('партиал ',rec.PartialResult())


        except KeyboardInterrupt:
            print('\nDone')
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))

    def from_file(self, file_name, sender = "file:"):
        def ff(self, file_name, sender = "file:"):
            SetLogLevel(0)
            #sample_rate = 16000
            #model = Model(lang="ru")
            #rec = KaldiRecognizer(model, sample_rate)
            rec = self.rec
            process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                        file_name,
                                        '-ar', str(self.sample_rate), '-ac', '1', '-f', 's16le', '-'],
                                       stdout=subprocess.PIPE)
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    print(rec.Result())
                else:
                    print(rec.PartialResult())

            self.recognized(rec.FinalResult(), sender+file_name)
    def recognized(self, *args):
        print(args)


class SpeechToText(STTVosk):
    def __init__(self, *args, **kwargs):
        super(SpeechToText, self).__init__(*args, **kwargs)
        self.out_call = None
        self.threc = None

    def bind(self, out_func):
        self.out_call = out_func

    def recognized(self, text, *args):
        if self.out_call:
            self.out_call(text, *args)
        else:
            print("# not binded: ", text)

    def start(self):
        if not self.threc:  # защита от двоиного запуска
            self.threc = Thread(target=self.mic_listen, name="Noname")
            self.threc.start()

    def stop(self):
        self.mic_listen_stop()
        if self.threc:
            self.threc.join()
        self.threc = None


'''
va = STTVosk()
va.mic_listen()
'''