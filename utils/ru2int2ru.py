# korol4ik
# int2ru(int)
# ru2int(str)


units = (
    "ноль",
    # исключение однО яблоко (ср.род)
    ("один", "одна"),
    ("два", "две"),

    "три", "четыре", "пять",
    "шесть", "семь", "восемь", "девять"
)

teens = (
    "десять", "одиннадцать",
    "двенадцать", "тринадцать",
    "четырнадцать", "пятнадцать",
    "шестнадцать", "семнадцать",
    "восемнадцать", "девятнадцать"
)

tens = (
    "двадцать", "тридцать",
    "сорок", "пятьдесят",
    "шестьдесят", "семьдесят",
    "восемьдесят", "девяносто"
)

hundreds = (
    "сто", "двести",
    "триста", "четыреста",
    "пятьсот", "шестьсот",
    "семьсот", "восемьсот",
    "девятьсот"
)

# множественное число и род
orders = (
    ("тысяча", "тысячи", "тысяч"),
    ("миллион", "миллиона", "миллионов"),
    ("миллиард", "миллиарда", "миллиардов"),
)

minus = "минус"


# int2ru
def under_hundred(dig: (int, str), gender="m"):
    if int(dig) == 0:
        return ""
    # проверка входных данных
    try:
        dig = int(dig)
    except ValueError as e:
        raise e
    if dig > 99:
        raise ValueError('argument must be less than 100')
    # ---
    # мужской род "m" - индекс кортежа [0], женский "f" (или любой не "m") [1]
    gen_idx = 0 if gender == "m" else 1

    if dig < 20:
        over_twenty = units + teens
        ru_txt = over_twenty[dig]

        # 1 и 2 нужен род, выбираем правильное слово из кортежа
        if isinstance(ru_txt, tuple):
            ru_txt = ru_txt[gen_idx]
        return ru_txt
    else:  # from 20 to 99
        units_ru = units[dig % 10]  # единицы
        # 1 и 2 нужен род, выбираем правильное слово из кортежа
        if isinstance(units_ru, tuple):
            units_ru = units_ru[gen_idx]
        if dig % 10 == 0:  # ноль в конце десятков
            units_ru = ""  # ненужен (20 = двадцать ноль)
        tens_ru = tens[dig // 10 - 2]  # десятки
        ru_txt = tens_ru + " " + units_ru
        return ru_txt


def under_thousand(dig: (int, str), gender='m'):
    try:
        dig = int(dig)
    except ValueError as e:
        raise e
    if dig > 999:
        raise ValueError('argument must be less than 1000')
    dig_str = str(dig)
    hundred = ''
    if len(dig_str) == 3:
        h_index = int(dig_str[0]) - 1
        hundred = hundreds[h_index]
        dig_str = dig_str[1:]

    undhund = under_hundred(dig_str, gender)
    return hundred + " " + undhund


def int2ru(number: int, gender="m"):
    if number == 0:
        return units[0]
    minus_word = minus if number < 0 else ""
    # словарь следования
    # billion, million, thousand, hundreds, under hundred
    num_str = str(abs(number))
    lenum = len(num_str)
    ords = lenum // 3
    len_next = lenum % 3
    ru_number_string = ''  # under_hundred(num_str[:lenfist]) if lenfist > 0 else ''
    start = 0
    # print(ords,lenfist)
    for i in range(ords, -1, -1):
        if len_next:
            gen = 'f' if i == 1 else 'm'
            if i == 0:
                gen = gender
            to_pars_uh = num_str[start:start+len_next]
            start += len_next
            order_num = ""
            unthous = under_thousand(to_pars_uh, gender=gen)
            if i > 0:  # bmt
                order = orders[i-1]
                order_num = order[2]
                if to_pars_uh.endswith("1") and not to_pars_uh.endswith("11"):  # unhint ==1
                    order_num = order[0]
                if to_pars_uh.endswith(("2", "3", "4")) and not to_pars_uh.endswith(("12", "13", "14")):
                    order_num = order[1]
                # убрать "один" из: миллиард, миллион, тысяча
                if int(to_pars_uh) == 1:
                    unthous = ""
            ru_number_string += " " + unthous + " " + order_num
        len_next = 3
    ru_number_string = minus_word + ru_number_string
    return ru_number_string.strip()


# числительные
def int2numeric_ru(number: int, gender="m"):

    numic_units = [
        "нулевой",
        "первый", "второй", "третий", "четвёртый", "пятый",
        "шестой", "седьмой", "восьмой", "девятый"
    ]

    numic_teens = [
        "десят", "одиннадцат",
        "двенадцат", "тринадцат",
        "четырнадцат", "пятнадцат",
        "шестнадцат", "семнадцат",
        "восемнадцат", "девятнадцат"
    ]

    numic_tens = [
        "двадцат", "тридцат",
        "сороковой",
        "пятидесят",
        "шестидесят", "семидесят",
        "восьмидесят", "девяност"
    ]

    numic_hudres = [
        "сот", "двухсот",
        "трёхсот", "четырёхсот",
        "пятисот", "шестисот",
        "семисот", "восьмисот",
        "девятисот"
    ]

    numeric_orders = [
        "тысячн", "миллионн", "миллиардн"
    ]

    # gender = "m" #mfn"  # мужской, женский, средний
    endet = "ый"
    if gender == "f":
        endet = "ая"
    if gender == "n":
        endet = "ое"

    if gender != "m":
        numic_units = [nu[:-2] + endet for nu in numic_units]
        if gender == "f":
            numic_units[3] = numic_units[3][:-2] + "ья"
        if gender == "n":
            numic_units[3] = numic_units[3][:-2] + "ье"

    def add_ends(lst, ends):
        return list(el + ends for el in lst)

    numic_teens = add_ends(numic_teens, endet)
    if gender == "m":
        numic_tens = add_ends(numic_tens, endet)
        numic_tens[2] = numic_tens[2][:-2]
    else:
        numic_tens[2] = numic_tens[2][:-2]
        numic_tens = add_ends(numic_tens, endet)

    numic_hudres = add_ends(numic_hudres, endet)
    numic_orders = add_ends(numeric_orders, endet)
    numeric_twenty = numic_units + numic_teens

    if abs(number) < 20:  # minus??
        return numeric_twenty[number]
    lastwo = int(str(number)[-2:])
    if 0 < lastwo < 20:
        return numeric_twenty[lastwo]
    ords = 0
    dig = 0
    for d in str(number)[::-1]:
        if int(d) == 0:
            ords += 1
        else:
            dig = int(d)
            break

    last_numeric = ""
    if ords == 0:  # единицы
        last_numeric = numic_units[dig]
    if ords == 1:  # десятки > 10
        last_numeric = numic_tens[dig-2]
    if ords == 2:  # сотни
        last_numeric = numic_hudres[dig-1]
    if 3 <= ords < 6:
        last_numeric = numic_orders[0]
    if 6 <= ords < 9:
        last_numeric = numic_orders[1]
    if 9 <= ords < 12:
        last_numeric = numic_orders[2]
    numeric_number = int2ru(number).split()[:-1] + [last_numeric]
    # print(numic_orders, numic_hudres, numic_tens, numic_teens, numic_units)
    return ' '.join(numeric_number)


#  Текст в инт #
#
#  преобразует кортежи в словарь: { "один" : 1, "одна": 1, "два": 2 ...}
def dig_name_dict(tuple_nums, start: int, step: int):
    dict_names = {}
    for i, num in enumerate(tuple_nums):
        if isinstance(num, tuple):
            for n in num:
                dict_names.update({n: start + step*i})
        else:
            dict_names.update(({num: start + step*i}))
    return dict_names
# ---


# Словарь всех числительных
all_dig_names = {}

units_d = dig_name_dict(units, 0, 1)
all_dig_names.update(units_d)

teens_d = dig_name_dict(teens, 10, 1)
all_dig_names.update(teens_d)

tens_d = dig_name_dict(tens, 20, 10)
all_dig_names.update(tens_d)

hundreds_d = dig_name_dict(hundreds, 100, 100)
all_dig_names.update(hundreds_d)

orders_d = dig_name_dict(orders[0], 1000, 0)
all_dig_names.update(orders_d)

orders_d = dig_name_dict(orders[1], 1_000_000, 0)
all_dig_names.update(orders_d)

orders_d = dig_name_dict(orders[2], 1_000_000_000, 0)
all_dig_names.update(orders_d)
# -------


# rules {dca, db}, {}g{}f{}e{}
def get_range(number: int):
    if 0 <= number < 10:
        return "a"
    if 10 <= number < 20:
        return "b"
    if 20 <= number < 100:
        return "c"
    if 100 <= number < 1000:
        return "d"
    if 1000 <= number < 1000_000:
        return "e"
    if 1000_000 <= number < 1000_000_000:
        return "f"
    if 1000_000_000 <= number < 1000_000_000_000:
        return "g"
    if number >= 1000_000_000:
        return "z"


def hund_rules(abcd):
    per_hnd = ("a", "b", "c", "ca", "d", "da", "db", "dc", "dca")
    out = ""
    rest = abcd
    while rest:
        alen = 3 if len(rest) > 3 else len(rest)
        if rest[:alen] in per_hnd:
            out += rest[:alen] + ","
            rest = "" if len(rest) == alen else rest[alen:]
        else:
            while alen > 0:
                if rest[:alen] in per_hnd:
                    out += rest[:alen] + ","
                    rest = "" if len(rest) == alen else rest[alen:]
                elif alen == 1:
                    if out.endswith(","):
                        out = out[:-1] + rest[0]
                    else:
                        out += rest[0]
                    rest = "" if len(rest) == alen else rest[alen:]
                    # raise ValueError('symbol not in abcd')
                alen += -1
    # out = out[:-1] if out[-1] == "," else out
    return out


def parse_int_list(int_list):
    # res_dict = { i: get_range(dig) for i, dig in enumerate(int_list) if isinstance(dig, int)}
    # разбиваем на части
    start = 0
    res = []
    lil = len(int_list)
    for i, dig in enumerate(int_list):
        if not dig:
            continue
        if i > 0 and not int_list[i-1]:  # предыдущий пустой, начало записи
            start = i
        # следующий пустой или это последний, завершаем
        if (i+1 < lil and not int_list[i+1]) or i+1 == lil:
            res.append(int_list[start:i+1])

    entries = []  # текстовое представление
    for nn in res:
        entry = []
        for d in nn:
            entry.append(get_range(d))
        entries.append(''.join(entry))

    # проверка на большее число после меньшего (тысячи, миллионы, миллиарды)
    # при перечислении чисел, возможна не корректная разбивка
    # тысяча сто тысяч = 1100, 1_000_000
    # жадный алгоритм и не определяет род числительного (возможно улучшить)
    order = "gfe"

    per_hund = [hund_rules(ent) for ent in entries]  # буквенное выражение числительных
    br_pos = []
    for i, ent in enumerate(per_hund):
        o_start = -1
        for j, e in enumerate(ent):
            o_pos = order.find(e)
            if o_pos >= 0:
                if o_pos >= o_start:
                    o_start = o_pos
                else:
                    br_pos.append([i, j])
                    o_start = -1
    for i, j in br_pos:
        per_hund[i] = per_hund[i][:j] + ',' + per_hund[i][j:]
    per_nums = ''.join(per_hund).strip(",")
    # буквенное выражение числительных разбитые на группы запятыми
    # разбивка int_list по шаблону pre_hund
    n = 0
    to_sum = []
    for num in per_nums.split(","):
        while not int_list[n]:
            to_sum.append(int_list[n])
            n += 1
            if n == len(int_list):
                break
        if n == len(int_list):
            break
        to_sum.append(int_list[n:n+len(num)])
        n += len(num)

    # to_sum += ([''] * (len(int_list) - n))
    # суммирование / умножение
    nums_list = []
    for ts in to_sum:
        n_sum = 0
        hnd_ = 0
        if not isinstance(ts, list):
            nums_list.append(ts)
            continue
        for num in ts:
            if num < 1000:
                hnd_ += num
            else:
                n_sum += hnd_ * num if hnd_ else num
                hnd_ = 0
        n_sum += hnd_
        nums_list.append(n_sum)

    '''
    print('int_list ', int_list)
    print('res ', res)
    print('entries ', entries)
    print('per_nums ', per_nums)
    print('to_sum', to_sum)
    print('nums_list', nums_list)
    '''
    return nums_list, to_sum


def ru2int(txt):
    int_list = []
    s_text = txt.split()
    # распознать все числительные в строке
    for word in s_text:
        if word in all_dig_names:
            int_list.append(all_dig_names[word])
        else:
            int_list.append('')
    # ---
    parsed_string, to_sum = parse_int_list(int_list)
    # заменяем цифры в тексте
    # to_sum такой же размерности как и s_text

    out_list = []
    n = 0
    for i, ts in enumerate(to_sum):
        if ts == '':
            out_list.append(s_text[n])
        elif ts == 0:
            out_list.append(str(0))
        elif isinstance(ts, list):
            n += (len(ts) - 1)
            out_list.append(str(parsed_string[i]))

        n += 1
    while n < len(s_text):
        out_list.append(s_text[n])
        parsed_string.append(int_list[n])
        n += 1
    return " ".join(out_list), parsed_string


'''
text_num = "это привет как вас там ноль там сто семьдесят шесть семьдесят там сорок семьдесят четыре , сорок кажется да"
print(text_num)
text, nums = ru2int(text_num)  # _num)
digits = [int2ru(num, "f") for num in nums if not num == ""]
print(text)
print(nums)
print(digits)
'''