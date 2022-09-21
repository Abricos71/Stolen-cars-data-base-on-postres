from itertools import cycle
from Code import db_logic
from Message import status_print
eng_alpa_low = 'abcdefghijklmnopqrstuvwxyz'
key = 'sometextdontworryitisnotkeyitisdiesnmattergogodonotlookatthis'
rus_alf = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
rus_key = 'этопростотекстнеключосвсемнеключ'


def admin_login(login, password):
    db_logic.conn()
    if password == decode(db_logic.get_pas_value(encode(login), 0)):
        status_print('True')
        return(True)
    else:
        status_print('неправильный логин или пароль')
        return (False)
    db_logic.end_of_work()


# кодирование данных пользователя
def encode(letters_to_enc):
    return ''.join(map(lambda arg: eng_alpa_low[(eng_alpa_low.index(arg[0]) + eng_alpa_low.index(arg[1]) % 26) % 26], zip(letters_to_enc, cycle(key))))


# декодирование данных пользователя
def decode(letters_to_dec):
    return ''.join(map(lambda arg: eng_alpa_low[eng_alpa_low.index(arg[0]) - eng_alpa_low.index(arg[1]) % 26], zip(letters_to_dec, cycle(key))))


def rus_encode(rus_text):
    return ''.join(map(lambda arg: rus_alf[(rus_alf.index(arg[0]) + rus_alf.index(arg[1]) % 33) % 33], zip(rus_text, cycle(rus_key))))


# декодирование данных пользователя
def rus_decode(rus_text):
    return ''.join(map(lambda arg: rus_alf[rus_alf.index(arg[0]) - rus_alf.index(arg[1]) % 33], zip(rus_text, cycle(rus_key))))
