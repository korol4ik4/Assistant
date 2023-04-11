from network.server import Server
from assistent import Assistant
from message import Message
class TerminalAssistant(Assistant):

    def __init__(self,address='127.0.0.1', port=5555):
        super(TerminalAssistant,self).__init__()
        self.server = Server(address=address, port=port,timeout=None)
        self.server.incoming = self.incoming
        self.conn = None
        self._list_event = False
        self._event_sender = []
        self._list_task = False
        self._task_actor = []


    def incoming(self, service_message, data, connect):

        srv_msg = Message(service_message)

        if srv_msg.data_type == 'message':
            message = data.decode()

            answer = self.terminal_executer(message)

            self.server.send_data(connect, str(answer).encode(), data_type="message")
            self.conn = connect
            #print(f"received: {service_message}' \ndata = {data}")
        else:
            print("fail service message: ", service_message)

    def event_list(self,*args):
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
        else:
            self._list_event = True  # default 'all'

        if not self._list_event:
            return "not listen events"
        if self._event_sender:
            return f'listen events from {self._event_sender}'
        else:
            return 'listen all events'
    # --------------------------------------------
    def task_list(self, *args):
        if len(args) == 0:
            return self.task_list_()
        elif len(args) == 1:
            if args[0] == 'all':
                self._task_actor = []
                self._list_task = True
            elif args[0] == 'nix':
                self._list_task = False
            elif args[0] in self.all_plugins.keys():
                self._task_actor.append(args[0])
                self._list_task = True
        else:
            self._task_actor = [name for name in args if name in self.all_plugins.keys()]
            if self._task_actor:
                self._list_task = True

        if not self._list_task:
            return "not listen tasks"
        if self._task_actor:
            return f'listen tasks for {self._task_actor}'
        else:
            return 'listen all tasks'

    # --------------------------------------------
    #virtual func from Assistant
    def on_event(self, new_event):

        if self._list_event:
            if not self._event_sender:
                if self.conn:
                    self.server.send_data(self.conn,str(new_event()).encode(), data_type="message")
                else:
                    print('Terminal new event ', new_event())
            elif 'sender' in new_event():
                if isinstance(self._event_sender, (list,tuple)):
                    if new_event.sender in self._event_sender:
                        if self.conn:
                            self.server.send_data(self.conn,str(new_event()).encode(), data_type="message")
                        else:
                            print('Termina new event ', new_event())
    # virtual func from Assistant
    def on_task(self, plugin_name, msg):
        outstr = 'Termina new task for {0} msg {1}'.format(plugin_name,msg())
        if self._list_task:
            if not self._task_actor:
                if self.conn:
                    self.server.send_data(self.conn, outstr.encode() , data_type="message")
                else:
                    print(outstr)
            if isinstance(self._task_actor, (list,tuple)):
                if plugin_name in self._task_actor:
                    if self.conn:
                        self.server.send_data(self.conn, outstr.encode() , data_type="message")
                    else:
                        print(outstr)

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
            dstr = dstr.replace("'","")
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
        # event add {sender: STT, text: Hello world, lang : en}
        # [1,1,(),{kw}]

        # event list all/nix
        # [1,2,('all',),]

        # event list STT
        # [1,2,('SST',),{}]

        # event list STT TERMINAL TTS
        # [1,2,('STT','TERMINAL','TTS'),{}]
        '''------------------'''
        # task add SENDER ACCEPTOR {text: * }
        # [2,1,('SENDER','ACCEPTOR',), {text:'*'}]

        # task list
        # [2,2,(){}]

        # task list all/nix
        # [2,2,('all',){}]

        # task list STT
        # [2,2,('SST',){}]

        # task list STT TERMINAL TTS
        # [2,2,('SST','TERMINAL','TTS'){}]

        # task delete SENDER TERMINAL (text,lang,)
        # [2,3,('SENDER','TERMINAL', field,key,list)]
        # task delete all
        '''------------------'''
        # loop start
        # [3,1,(),{}]
        # loop stop
        # [3,2,(),{}]
        # loop pause
        # [3,3,(),{}]
        # loop status
        # [3,4,(),{})
        '''------------------'''
        # plugin list loaded/imported/all
        # [4,1,('loaded/imported/all'){}]

        # plugin import path # all plug_*.py files from order
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
            commands = ("event", "task", "loop", "plugin", "help")
            if not cmd or not all(cmd) or cmd[0] not in commands:
                return [command_num, option_num, args, kwargs] # нет комманды

            command_num = commands.index(cmd[0])+1
            # options[command_num] = (options of command)
            options = (("add", "list"),  # event
                       ("add", "list", "delete"),  # task
                       ("start", "stop","pause", "status"),  # loop
                       ("list", "import", "load", "close"), # plugin
                       ("","event", "task", "loop", "plugin"),)  # help

            if len(cmd) < 2:
                # пустая опция - тоже опция, например help
                if "" in options[command_num-1]:
                    option_num = options[command_num-1].index("")+1
                return [command_num, option_num, args, kwargs]
            elif cmd[1] not in options[command_num-1]:
                #print("# нет опции / неизвестная опция")
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
        #print(param)
        cmd, opt, args, kwargs = param

        if not (cmd and opt):  # else: cmd and opt > 0
            return self.terminal_executer("help")
        #[1,2] ("add", "list"),  # event
        #[2,3] ("add", "list", "delete"),  # task
        #[3,2] ("start", "stop"),  # loop
        #[4,4] ("list", "import", "load", "close"))  # plugin
        if cmd == 1:  # event
            if opt == 1:  # add
                if kwargs: # kwargs
                    return self.event_add(kwargs)  #add new event
                else:
                    return f"nothing to add, kwargs = {kwargs}"

            elif opt ==2:  # list
                return self.event_list(*args)

        elif cmd == 2:  # task
            if opt == 1:  # add
                if len(args) == 2:
                    sender, acceptor = args
                    return self.task_add(sender, acceptor, **kwargs)
                else:
                    return "invalid number of arguments\n use '>help task add"  # неподходящие кол-во аргументов
            elif opt == 2:  # list
                return self.task_list(*args)

            elif opt == 3:  # delete
                if not args:
                    return "nothing to delete"  # нечего удалять
                return  self.task_del(*args)

        elif cmd == 3:  # loop
            if opt == 1:  # start
                return self.loop_start()
            elif opt == 2:  #stop
                return self.loop_stop()
            elif opt == 3:  # pause
                return self.loop_pause()
            elif opt == 4:  # status
                return self.loop_stat()


        elif cmd == 4:  # plugin
            if opt == 1:  #list
                return self.plugin_list(*args)
            elif opt == 2:  # import
                if not args:  # нет пути(папки) для импорта
                    return "Don't find path"
                else:
                    return self.import_plugins_from_path(args[0])
            elif opt == 3:  #load
                if not args:  # нет имени плагина ( или all)
                    return "no plugin name or all"
                return self.load_plugins(*args)

            elif opt == 4:  # close
                return self.close_plugin(*args)


        elif cmd == 5:  # help
            options = (("add", "list"),  # event
                       ("add", "list", "delete"),  # task
                       ("start", "stop", "pause", "status"),  # loop
                       ("list", "import", "load", "close"),  # plugin
                       ("", "event", "task", "loop", "plugin"),)  # help
            if opt == 1:  # ""
                return f"possible commands: {', '.join(options[4][1:])}"
            elif opt == 2:  # event
                if not args or args[0] not in options[0]:
                    #print(*args,options[0])
                    return f"possible options for event: {', '.join(options[0])}"
                else:
                    out_str = ""
                    if "add" in args:
                        out_str += "event add event\n"
                        out_str += "Example:\n"
                        out_str += "{sender: STT, text: Hello world, lang : en}"
                    elif "list" in args:
                        out_str += "event list all/nix/PLUGIN_NAME\n"
                        out_str += "Example:\n"
                        out_str += "event list STT TERMINAL TTS\n"
                        out_str += "event list STT\n"
                        out_str += "event list nix"
                    return out_str

            elif opt == 3:  # task
                if not args or args[0] not in options[0]:
                    out_str = f"possible options for task : {', '.join(options[1])}, help\n"
                    return out_str
                else:
                    out_str = ""
                    if "add" in args:
                        out_str += "task add SENDER ACCEPTOR \n"
                        out_str += "SENDER - name of plugin. Events creator \n"
                        out_str += "ACCEPTOR - name of plugin. Events receiver\n"
                        out_str += "Example:\n"
                        out_str += "task add TTS STT {text: * }"
                        out_str += "simple repeater :)"
                    elif "list" in args:
                        out_str += "task list all/nix/PLUGIN_NAME\n"
                        out_str += "Example:\n"
                        out_str += "task list STT TERMINAL TTS\n"
                        out_str += "task list STT\n"
                        out_str += "task list nix\n"
                        out_str += "without options returned current list of tasks\n"
                        out_str += "task list"
                    elif "delete" in args:
                        out_str += "task delete SENDER ACCEPTOR (keywords,) \n"
                        out_str += "task delete all\n"
                        out_str += "Example:\n"
                        out_str += "task delete STT TTS"
                    return out_str
            elif opt == 4:  # loop
                out_str =  f"possible options for loop: {', '.join(options[2])}\n"
                if args:
                    out_str += "loop options have not arguments"
                return out_str

            elif opt == 5:  # plugin
                if not args or args[0] not in options[0]:
                    return f"possible options for plugin: {', '.join(options[3])}"
                else:
                    out_str = ""
                    if "list" in args:
                        out_str += "plugin list loaded/imported/all"
                    elif "import" in args:
                        out_str += "plugin import path\n"
                        out_str += "# all plug_*.py files from order"
                    elif "load" in args:
                        out_str += "plugin load <NAME OF PLUGINS>\n"
                        out_str += "Example:\n"
                        out_str += "plugin load STT TERMINAL TTS\n"
                        out_str += "plugin load all"
                    elif "close" in args:
                        out_str += "plugin close <NAME OF PLUGINS>"
                        out_str += "Example:\n"
                        out_str += "plugin close STT TERMINAL TTS\n"
                        out_str += "plugin close all"
            else:
                return param
        return param


    def loop_input(self):
        text =''
        while text != 'exit':
            text=input('>')
            #msg = Message(sender='TERMINAL',text=text,lang='en')
            #Plugin.event.add(msg)
            print(self.terminal_executer(text))
        self.loop_stop()









