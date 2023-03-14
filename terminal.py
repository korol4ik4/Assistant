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

    def loop_stop(self):
        self.started = False
        self.paused = False
        self.thr_loop.join()
        self.thr_loop = None
    def loop_start(self):
        self.paused = False
        print('loop started ', self.started)
        if self.started:
            return

        if len(self.all_plugins):
            for name, plug in self.all_plugins.items():
                plug.close()
        self.all_plugins = {}
        self.load_plugins(path="plugin")  # имя директории с файлами плагинов
        print(self.thr_loop)
        if not self.thr_loop:  # защита от двоиного запуска
            self.thr_loop = Thread(target=self.loop, name="AssistentMainLoop")
            self.thr_loop.start()
        else:

            self.thr_loop.start()


    def task_add(self, sender, acceptor, **kwargs):
        print(sender, acceptor, kwargs)
        if not kwargs:
            kwargs = {'text':'*'}
        new_task = {sender:{acceptor: kwargs} }
        Plugin.task.update(new_task)

    def task_list(self):
        return Plugin.task()

    def task_del(self,evn_creator, acceptor = None, *args):
        Plugin.task.delete(evn_creator, acceptor, *args)

    def event_add(self,message:dict):
        msg = Message(**message)
        Plugin.event.add(msg)

    '''    
    def task_list_all(self, _list=True):
        self._list_task = _list
    def event_list(self, _list=True):
        self._list_event = _list
    '''

    #virtual func from Assistant
    def on_event(self, new_event:Message):
        if self._list_event:
            if not self._event_sender:
                print('Terminal new event ', new_event())
            elif 'sender' in new_event():
                if isinstance(self._event_sender, (list,tuple)):
                    if new_event.sender in self._event_sender:
                        print('Termina new event ', new_event())
    # virtual func from Assistant
    def on_task(self, plugin_name, msg:Message):
        if self._list_task:
            if not self._task_actor:
                print('Termina new task for {0} msg {1}'.format(plugin_name,msg()))
            if isinstance(self._task_actor, (list,tuple)):
                if plugin_name in self._task_actor:
                    print('Termina new task for {0} msg {1}'.format(plugin_name,msg()))
    @staticmethod
    def terminal_parser(terminal_input):
        def brace(istr: str, brace='{}'):

            if len(brace) != 2:
                return istr, None
            open_brace = istr.find(brace[0])
            if open_brace >= 0:
                close_brace = istr.rfind(brace[1])
                if close_brace > open_brace:
                    brace_content = istr[open_brace + 1:close_brace]
                    return istr[:open_brace], brace_content
            return istr, None

        # str =" key1 :value1,key2: value2"
        def str2dict(dstr):
            out_dict = {}
            itms = dstr.split(',')
            try:
                for itm in itms:
                    if not itm:
                        continue
                    key, value = itm.split(':')
                    out_dict.update({key.strip(): value.strip()})
            except:
                print("can't " + dstr + ' to dict')
            return out_dict

        def token(tinput: str):
            txt, brace_conent = brace(tinput)
            dict_value = str2dict(brace_conent) if brace_conent else {}
            cmd_line = txt.split()
            return cmd_line, dict_value

        # positive test parser
        '''------------------'''
        # event add {sender: SST, text: Hello world, lang : ru}
        # [1,1,(),{kw}]

        # event list all/nix
        # [1,2,('all',),]

        # event list SST
        # [1,2,('SST',),{}]

        # event list SST TERMINAL TTS
        # [1,2,('SST','TERMINAL','TTS'),{}]
        '''------------------'''
        # task add SENDER ACCEPTOR {text: * }
        # [2,1,('SENDER','ACCEPTOR',), {text:'*'}]

        # task list
        # [2,2,(){}]

        # task list all/nix
        # [2,2,('all',){}]

        # task list SST
        # [2,2,('SST',){}]

        # task list SST TERMINAL TTS
        # [2,2,('SST','TERMINAL','TTS'){}]

        # task delete SENDER TERMINAL (text,lang,)
        # [2,3,('SENDER','TERMINAL', field,key,list)]
        '''------------------'''
        # loop start
        # [3,1,(){}]
        # loop stop
        # [3,2,(){}]
        # loop pause
        # [3,3,(){}]
        '''------------------'''
        # plugin list loaded/imported/all
        # [4,1,('loaded/imported/all'){}]

        # plugin import modul path.withouts.pace
        # [4,2, (path){}]

        # plugin load NAME SST
        # [4,3, ('NAME','SST'){}]

        # plugin close NAME
        # [4,4, ('NAME',){}]
        '''------------------'''

        def parser(tinput:str):
            cmd, kwargs = token(tinput)
            command_num = 0
            option_num = 0
            args = ()
            commands = ("event", "task", "loop", "plugin")
            if not cmd or not all(cmd) or cmd[0] not in commands:
                return [command_num, option_num, args, kwargs] # нет комманды

            command_num = commands.index(cmd[0])+1
            # options[command_num] = (options of command)
            options = (("add", "list"),  # event
                       ("add", "list", "delete"),  # task
                       ("start", "stop","pause"),  # loop
                       ("list", "import", "load", "close"))  # plugin

            if len(cmd) < 2 or not (cmd[1] in options[command_num-1]):
                print("# нет опции / неизвестная опция")
                return [command_num, option_num, args, kwargs] # нет опции / неизвестная опция
            #print("options[command_num-1], options[command_num-1].index(cmd[1]) +1 ", options[command_num-1], options[command_num-1].index(cmd[1]) +1, cmd[1])
            option_num = options[command_num-1].index(cmd[1])+1
            if len(cmd)>2:
                args = cmd[2:]
            return [command_num, option_num, args, kwargs]  # полный вывод
        #out parser
        # [num_of_command, num_of_option, *args,**kwargs]

        return parser(terminal_input)



    def terminal_executer(self,terminal_input:str):
        # [num_of_command, num_of_option, *args,**kwargs]
        param = self.terminal_parser(terminal_input)
        print(param)
        cmd, opt, args, kwargs = param

        if not (cmd and opt):  # else: cmd and opt > 0
            self.terminal_error(param)
            return
        #[1,2] ("add", "list"),  # event
        #[2,3] ("add", "list", "delete"),  # task
        #[3,2] ("start", "stop"),  # loop
        #[4,4] ("list", "import", "load", "close"))  # plugin
        if cmd == 1:  # event
            if opt == 1:  # add
                if kwargs: # kwargs
                    self.event_add(kwargs)  #add new event
            elif opt ==2:  # list
                self._event_sender = []
                if args:
                    if args[0] == 'all':
                        self._list_event = True
                    elif args[0] == 'nix':
                        self._list_event = False
                    else:  # names of Plugin
                        # test: Plugin with name is loaded
                        self._event_sender = [name for name in args if name in self.all_plugins.keys()]
                        if self._event_sender:
                            self._list_event = True
                        #self.event_list(names_to_list)
                else:
                    self._list_event = True  # default 'all'

        elif cmd == 2:  # task
            if opt == 1:  # add
                if len(args) == 2:
                    sender, acceptor = args
                    print(sender, acceptor, kwargs)
                    self.task_add(sender, acceptor,**kwargs)
                else:
                    self.terminal_error(param)  # неподходящие кол-во аргументов
            elif opt == 2:  # list
                if len(args) == 0:
                    print(self.task_list())
                elif len(args) == 1:
                    if args[0] == 'all':
                        self._list_task = True
                    elif args[0] == 'nix':
                        self._list_task = False
                    elif args[0] in self.all_plugins.keys():
                        self._task_actor.append(args[0])
                else:
                    self._task_actor = [name for name in args if name in self.all_plugins.keys()]
                    if self._task_actor:
                        self._list_task = True
            elif opt == 3:  # delete
                if not args:
                    self.terminal_error(param)  # нечего удалять
                    return
                sender = None
                acceptor = None
                field_name = []
                if len(args) == 1:
                    sender = args[0]
                elif len(args) > 1:
                    sender, acceptor, *field_name = args
                    field_name = [] if not field_name else field_name[0]
                self.task_del(sender,acceptor,field_name)
        elif cmd == 3:  # loop
            if opt == 1:  # start
                self.loop_start()
            elif opt == 2:  #stop
                self.loop_stop()
            elif opt == 3:  # pause
                self.paused = True
        elif cmd == 4:  # plugin
            if opt == 1:  #list
                if len(args) == 0:  # default all
                    print('imported Plugins ', Plugin.__subclasses__())
                    print('loaded Plugins ', self.all_plugins)
                if len(args) == 1:
                    if args[0] == 'all':  # all
                        print('imported Plugins ', Plugin.__subclasses__())
                        print('loaded Plugins ', self.all_plugins)
                    elif args[0] == 'loaded':
                        print('loaded Plugins ', self.all_plugins)
                    elif args[0] == 'imported':
                        print('imported Plugins ', Plugin.__subclasses__())
            elif opt == 2:  # import
                if not args:
                    return
                else:
                    pass
        return


    def terminal_error(self, param):
        print("error ",param)



    def loop_input(self):
        text =''
        while text != 'exit':
            text=input('input text')
            #msg = Message(sender='TERMINAL',text=text,lang='en')
            #Plugin.event.add(msg)
            self.terminal_executer(text)






