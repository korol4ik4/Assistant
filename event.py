#
# Класс Событие хранит список при получении элемент (нулевой т.е. попавший первым) удаляется
class Event:
    def __init__(self):
        self.event_list = []

    def add(self, event):  # Добавить в список
        if isinstance(event, (list, tuple)):
            if len(event) == 2:
                self.event_list.append(event)
                return True
        return False

    def get(self):  # Получить и удалить
        if self.event_list:
            return self.event_list.pop(0)


'''
### Example ###
ev = Event()
for i in range(10):
    ev.add(i)

for i in range(11):
    print(ev.get())
'''