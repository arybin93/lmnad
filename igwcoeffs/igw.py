# -*- coding: utf-8 -*-


def handle_file(file, separator, max_row=None):
    # save file
    with open(file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    with open(file.name) as file:
        data = file.read()

    data = data.split('\n')
    if not max_row:
        max_row = len(data)

    result = []
    for i in range(0, max_row):
        parse_row = data[i].split(separator)
        row = []
        for element in parse_row:
            if len(element) > 1:
                row.append(element)
        result.append(row)

    if result:
        return True, result[:max_row], len(data)
    else:
        return False, 'EMPTY_FILE, 'u'Пустой файл'
