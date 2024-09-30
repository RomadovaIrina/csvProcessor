def parse_csv(data) -> list:
    parsed = []
    # Разделяем строки по символу переноса строки
    lines = data.strip().split('\n')
    # Выбираем из первой строки заголовки
    keys = lines[0].split(',')
    # Убираем лишние пробелы для каждого ключа
    keys = [key.strip() for key in keys]
    for line in lines[1:]:
        # Разделяем строку по запятым,
        # и убираем лишние проблемы для каждого элемента
        temp = [i.strip() for i in line.split(',')]
        # zip - пакуем массивы одинаковой длинны
        parsed.append(dict(zip(keys, temp)))
    return parsed
