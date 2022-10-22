#
# all Message property's must be a string

from message import Message

msg = Message(text="String", size=12, value=0.5, tup = ("tuple",),lst = ['list'])
print("class Message Test:")
for k,v in msg().items():
    print(k," = ", v)