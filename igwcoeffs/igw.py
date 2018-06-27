# -*- coding: utf-8 -*-


def handle_file(file, max_row=None):
    # save file
    with open(file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    with open(file.name) as file:
        data = file.read()

    data = data.split('\n')
    if not max_row:
        max_row = len(data)

    if data:
        return True, data[:max_row], len(data)
    else:
        return False, 'EMPTY_FILE, 'u'Пустой файл'
