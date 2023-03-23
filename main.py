from assistent import Assistant
from terminal import TerminalAssistant


my_assistent =   TerminalAssistant() # Assistant()

my_assistent.init_plugins()
my_assistent.loop_start()
#my_assistent.loop_input()
'''
my_assistent =  Assistant() # Assistant()
my_assistent.init_plugins()
my_assistent.loop_start()
'''