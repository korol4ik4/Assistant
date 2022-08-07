#
# all Message property's must be a string

from message import Message

msg = Message()
test_data = ("String", 12, 0.5, ("tuple",), [list])
print("class Message Test:")
t = 0
for i in range(len(test_data)):
    n = 0
    try:
        msg.text = test_data[i]
    except ValueError:
        if i > 0:
            n += 1
    try:
        msg.command = test_data[i]
    except ValueError:
        if i > 0:
            n += 1
    try:
        msg.sender = test_data[i]
    except ValueError:
        if i > 0:
            n += 1
    try:
        msg.file_name = test_data[i]
    except ValueError:
        if i > 0:
            n += 1

    if i == 0:
        if n == 0:
            print(format("Test 1 is ok"))
            t += 1
        else:
            print(format("Test 1 is fail"))
    else:
        if n == 4:
            print(format("Test {0} is ok".format(i+1)))
            t += 1
        else:
            print(format("Test {0} is fail".format(i+1)))

if t == 5:
    print("class Message Test is OK")
else:
    print("class Message Test is FAIL")