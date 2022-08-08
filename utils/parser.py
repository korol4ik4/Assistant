#
# Parser / Search functions

import re
from itertools import permutations

# Принимает текст и поисковый запрос вида:
# ? - заменяет 0 или 1 любой символ в слове
# * - 0 или любое другое кол- во символов в слове
# | - или (or) разделитель слов
# & - и (and) разделитель слов
#
def keyword_search(text, key):
    # преобразование key в регулярное выражение
    if not (key[0] in "*?"):
        key = r'\b' + key
    if not (key[-1] in "*?"):
        key += r'\b'
    key = key.replace("*", r'\w*')
    key = key.replace("?", r'\w?')
    key = key.replace("|", r'\b|\b')
    if "&" in key:
        and_keys = key.split("&")
        permut = permutations(and_keys)
        # key = key.replace("|", r'\b|\b')
        all_key = ''
        for variant in permut:
            all_key += r'(\b' + r'\b).*(\b'.join(variant) + ')|'
        if all_key.endswith('|'):
            key = all_key[:-1]
        else:
            key = all_key
    key = key.replace(r'\b\b', r'\b')
    # ----
    result = re.findall(key, text)
    # print("result ", result)
    result_key = []
    for key in result:
        # если был знак &, то результат-  список кортежей
        if isinstance(key, tuple):
            result_key += [k for k in key if k]
        else:
            result_key += [key]
    result_key = [k for k in result_key if k]
    return result_key
