#
# Базовый класс плагинов, переменные класса event и task (общий для всех) позволяют плагинам обмениваться сообщениями
# name - необходимое имя плагина по которому происходит обращение
# предложение использовать прописные(заглавные) из имени файла, без приставки plugin_
from plugin import Plugin
import logging
from message import Message
import datetime

class ChangeLanguagePlugin(Plugin):
    name = "LANGUAGE"  # необходимо переопределить в каждом плагине
      # можно переопределить для сохранения/ручного редактирования и загрузки настроек
    ling_lang = {'ru' : {'немец':'de','англи' : 'en'},
                 'de' : {'russ':'ru', 'engl' : 'en'},
                 'en' : {'russ':'ru', 'german' : 'de'}
                 }
    question = {'en' : 'what language to choose?',
                'ru' : 'какой язык выбрать?',
                'de' : 'welche sprache soll ich wählen?'
                }
    hello = {'en': 'hello',
                'ru': 'привет',
                'de': 'moin'
                }

    def __init__(self):
        super(ChangeLanguagePlugin, self).__init__()
        self.logger = logging.getLogger("Assistant.Plugin.Language")
        # подписать plugin to_name на события от текущего plugin self.name
        self.listen_from('NAME', text = '*мени язык*|sprach* *ände*|chang* lang*')
        self.talk_to('STT', command='language_*')
        self.talk_to('TTS',text='*')
        self.talk_to('CONTEXT', command='on_context')
        self.listen_from('CONTEXT', context='*')

        self.on_context = False

        # self.listen_from(self, from_name, keyword="*")  # подписаться на события от plugin from_name

    # Если plugin подписан на события, то при его возникновении Ассистент запускает эту функцию
    def find_lang(self,text, lang):
        if lang and (lang in self.ling_lang):
            new_lang = None
            lang_variant = self.ling_lang[lang]  #dict
            for lang_name, lang_prefix in lang_variant.items():
                if lang_name in text:
                    new_lang = lang_prefix
            if new_lang:
                return new_lang




    def exe_command(self, message):
        #self.logger.debug("listen from CONTEXT", self.task())
        if "lang" in message():
            new_lang = None
            txt =""
            if "text" in message():
                txt = message.text
            elif ('context' in message()) and self.on_context:
                txt = message.context

            new_lang = self.find_lang(txt, message.lang)
            if new_lang:
                self.post_message(command='language_' + new_lang)
                self.on_context = False
                self.post_message(text=self.hello[new_lang],lang=new_lang)
                return
            else:
                #self.not_listen_from('CONTEXT')

                self.on_context = True
                self.post_message(command='on_context')
                self.post_message(text=self.question[message.lang])