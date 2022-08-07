import json
import os


class Options(object):
    def __init__(self, name, default_options, path="options"):
        if not os.path.exists(path):
            os.mkdir(path)
        file_name = path + os.sep + name + ".json"
        self.options = {}
        if not isinstance(default_options, dict):
            raise ValueError("default_options must be dict")
        try:
            with open(file_name, 'r') as json_file:
                self.options = json.load(json_file)
        except FileNotFoundError:
            self.options = default_options
            self.update_options(file_name, default_options)

        '''if self.options.keys() != default_options.keys():
            self.update(file_name, default_options)
'''
    @staticmethod
    def update_options(file_name, data):
        try:
            with open(file_name, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(e, "\nDon't save to file ", file_name)

    def get(self):
        return self.options


"""
### Example ###
default_task = { # заглушка
        'STT': {
            "*" : "print"
    }}
Options(self.name, self.default_task,path="Commands").get()
"""
