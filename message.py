
#
# объект класса Message служит контейнером сообщений для событий event
# Message использовать JSON? - создаём стандартный словарь:
# Message = {{
#               'text' : '',
#               'command : '',
#               'message_sender' : '',
#               'file_name' : None  # null
#               'keywords' : ''
#               'port_in' : None
#               'port_out' : None
#           }}
# Обрезаем все не нужное с возможностью расширения
# Message = {
#               'message_sender' : '',
#               'text' : ''
#           }
#
# И абстрагируемся

class Message:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)
            return self.__dict__
        return self.__dict__


'''
# Example
msg = Message(message_sender = 'INPUT')
d1 = msg()
d2 = msg(text = "easy text")
msg.id = 15
# del msg.text
print(d1,"\n",d2,"\n")
# {'message_sender': 'INPUT', 'text': 'easy text', 'id': 15} 
# {'message_sender': 'INPUT', 'text': 'easy text', 'id': 15}
'''
