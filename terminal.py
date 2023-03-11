from threading import Thread

from assistent import Assistant
from plugin import Plugin
from message import Message
from utils.network.server import Server

class TerminalServer(Server):
    def __init__(self, addresse ='127.0.0.1', port=5555):
        super(TerminalAssistant).__init__(addresse=addresse,port=port)




class TerminalAssistant(Assistant):

    def __init__(self):
        super(TerminalAssistant,self).__init__()
        self._list_event = False
        self._event_sender = []
        self._list_task = False
        self._task_actor = []
        self.thr_loop = None




    def loop_start(self):
        if self.started:
            return
        if len(self.all_plugins):
            for name, plug in self.all_plugins.items():
                plug.close()
        self.all_plugins = {}
        self.load_plugins(path="plugin")  # имя директории с файлами плагинов
        if not self.thr_loop:  # защита от двоиного запуска
            self.thr_loop = Thread(target=self.loop, name="AssistentMainLoop")
            self.thr_loop.start()
        elif not self.thr_loop.isAlive():
            self.thr_loop.start()

    def task_add(self, new_task):
        Plugin.task.update(new_task)

    def task_rules(self):
        return Plugin.task()

    def task_list(self, _list=True):
        self._list_task = _list

    def task_del(self,evn_creator, acceptor = None, *args):
        Plugin.task.delete(evn_creator, acceptor, *args)

    def event_add(self,msg):
        Plugin.event.add(msg)

    def event_list(self, _list=True):
        self._list_event = _list


    #virtual func from Assistant
    def on_event(self, new_event:Message):
        if self._list_event:
            if not self._event_sender:
                print('Termina new event ', new_event())
            elif 'sender' in new_event():
                if isinstance(self._event_sender,str):
                    if new_event.sender == self._event_sender:
                        print('Termina new event ', new_event())
                elif isinstance(self._event_sender, (list,tuple)):
                    if new_event.sender in self._event_sender:
                        print('Termina new event ', new_event())
    # virtual func from Assistant
    def on_task(self, plugin_name, msg:Message):
        if self._list_task:
            if not self._task_actor:
                print('Termina new task for {0} msg {1}'.format(plugin_name,msg()))
            elif isinstance(self._task_actor,str):
                    if plugin_name == self._task_actor:
                        print('Termina new task for {0} msg {1}'.format(plugin_name,msg()))
            elif isinstance(self._task_actor, (list,tuple)):
                    if plugin_name in self._task_actor:
                        print('Termina new task for {0} msg {1}'.format(plugin_name,msg()))

    def loop_input(self):
        text =''
        while text != 'exit':
            text=input('input text')
            msg = Message(sender='TERMINAL',text=text,lang='en')
            Plugin.event.add(msg)






