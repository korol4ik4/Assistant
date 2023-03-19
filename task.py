#  Класс работает со словарём вида:
"""
default_task = { #
        'ИМЯ ПЛАГИНА': { # Передающего
            "keyword*" : "ИМЯ_ПЛАГИНА1,ПЛАГИН2" # Принимающий или несколько
    }}
"""


class Task:
    def __init__(self):
        self._muted_task = {}  # буфер (если плагину надо "захватить внимание")
        self._all_task = {}  # основной словарь
        self._not_muted_task = {}

    def mute_all(self):
        self._muted_task = self._all_task  # скидываем в буфер
        self._all_task = self._not_muted_task  # и добавляем не блокируемые задания как отмена

    def reset(self):
        self._all_task = self._muted_task  # достаём из буфера
        self._muted_task = {}  # отчищаем

    # создаёт ключ если нет
    # так же для вложенного списка,
    # добавляет значение в существующий через запятую или добавляет новый {ключ: значения}
    def update(self, task):
        if not isinstance(task,dict):
            return f"Тhe task must be a dictionary: {task}"
        for eventor, value in task.items():
            if not isinstance(value,dict):
                return f"wrong structure \nValue of eventor must be a dictionary: \n{eventor} : {value}"
            if eventor not in self._all_task:
                self._all_task.update({eventor:value})
                continue
            for acceptor in value:  #
                if acceptor not in self._all_task[eventor]:
                    self._all_task[eventor].update({acceptor: value[acceptor]})
                    continue
                else:
                    self._all_task[eventor][acceptor].update(value[acceptor])
        return f"task {task} successfully added"

    def __call__(self, *task):  # set/get через вызов объекта как функции
        if task:
            self.update(task[0])
        else:
            return self._all_task

    # Функции удаления из словаря
    def delete(self, event_creator:str, acceptor:str=None, *args):
        #print(event_creator, acceptor, args)
        if event_creator not in self._all_task:
            return False
        if not acceptor:
            self._all_task.pop(event_creator)
            return True
        if acceptor not in self._all_task[event_creator]:
            return False
        if not args or not args[0]:
            self._all_task[event_creator].pop(acceptor)
            if not self._all_task[event_creator]:
                self.delete(event_creator)
            return True
        ret = False
        for field in args:
            if field in self._all_task[event_creator][acceptor]:
                self._all_task[event_creator][acceptor].pop(field)
                ret = True
            if not self._all_task[event_creator][acceptor]:
                return self.delete(event_creator,acceptor)
        return ret