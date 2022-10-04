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
        for key, value in task.items():
            if key in self._all_task:
                keyword_dict = self._all_task[key]  # вложенный список основного словаря
                for keyword in value:  #
                    if keyword in keyword_dict:  # ключ вложенного словаря нового задания есть в основном словаре
                        val = self._all_task[key].pop(keyword)  # достаём ключ: значение
                        if value[keyword] not in val:  # если добавляемого значения нет в основном словаре
                            val += ("," + value[keyword])  # добавляем
                            self._all_task[key].update({keyword: val})  # обратно в основной словарь

                    else:  # нет в основном словаре, добавляем (вложенный словарь)
                        self._all_task[key].update({keyword: value[keyword]})
            else:  # нет в основном словаре, добавляем (верхний уровень)
                self._all_task.update({key: value})

    def __call__(self, *task):  # set/get через вызов объекта как функции
        if task:
            self.update(task[0])
        else:
            return self._all_task

    # Функции удаления из словаря
    def delete(self, event_creator, acceptor='', keyword=''):
        def extractor(word, comma_string):
            new_elements = [v for v in comma_string.split(",") if v != word and v]
            if new_elements:
                new_elements = ','.join(new_elements)
                return new_elements

        # state:
        # 0 - error, 1 - del_event_key, 2 - del_keyword,
        # 3 - del acceptor, 4 - del acceptor from keyword
        state = 0
        if event_creator:
            state += 1
            if keyword:
                state += 1
            if acceptor:
                state += 2
        # out_state:
        # 0 - ok(deleted), -1 - don't find event_key, -2 - don't find keyword,
        # -3 - don't find
        # print("state ", state)
        if state == 0:  # event_creator must be Name of Plugin
            return -1  # event_creator is '' or None or False etc.
        elif event_creator not in self._all_task:
            return -1  # event_creator not found

        if state == 1:
            self._all_task.pop(event_creator)
            return 0

        event_tasks = self._all_task[event_creator].copy()

        if state == 2:
            if keyword in event_tasks:
                self._all_task[event_creator].pop(keyword)
                return 0
            else:
                return -2
        if state == 4:
            if keyword not in event_tasks:
                return -2
            value = event_tasks[keyword]
            new_value = extractor(acceptor, value)
            if value == new_value:
                return -3
            if new_value:
                self._all_task[event_creator][keyword] = new_value
            else:
                self._all_task[event_creator].pop(keyword)
            return 0

        if state == 3:
            acc_fund = False
            for keyword, acceptors in event_tasks.items():
                if acceptor in acceptors:
                    new_value = extractor(acceptor, acceptors)
                    if acceptors == new_value:
                        return -3
                    if new_value:
                        self._all_task[event_creator][keyword] = new_value
                    else:
                        self._all_task[event_creator].pop(keyword)
                    acc_fund = True

            if acc_fund:
                return 0
            else:
                return -3


'''
### Example ###

t = Task()
#print(t())
task = {
        'STT' : {
    "ирин????" : 'name',
    "kot" : 'name,кот'
        },
        'Voice' : {
            '*' : 'admin'
}}

t(task)
#print(t())
task = {
        'STT' : {
    "ирин????" : 'бомж'}}
#t(task)
print(t())
t.del_admin('name', 'STT')
print(t())'''