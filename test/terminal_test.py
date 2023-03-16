from terminal import TerminalAssistant

TA = TerminalAssistant()
#
print('####################')
print('"plugin list all":')
print('#------------------#')
TA.terminal_executer('plugin list all')
input()

print('####################')
print('"plugin import ../plugin":')
print('#------------------#')
TA.terminal_executer('plugin import ../plugin')
input()


print('####################')
print('"plugin load STT TTS":')
print('#------------------#')
TA.terminal_executer('plugin load STT TTS')
input()

