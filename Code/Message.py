# функция вывода в терминал
def status_print(message):
    print('         ' + ((len(message) + 1) * '_'))
    print('       / ' + message + ' \\')
    print('      / ' + ((len(message) + 2) * '_') + '/')
    print('     |/')
    print('     "')
    print('^._.^ \n')
