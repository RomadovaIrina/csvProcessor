import re


def normalize_phone(phone_number) -> str:
    # Заменяем подходящее под паттерн на пустоту
    # заменяем все что является
    digits = re.sub(r'[^\d]', '', phone_number)
    if (digits[0] == '8'):
        digits = "7" + digits[1:]
    # Группируем первые 3 числа, вторые 3 числа и дальше по 2 числа,
    # чтобы привести к корректной форме вида +7(ххх)ххх-хх-хх
    return re.sub(r'7(\d{3})(\d{3})(\d{2})(\d{2})',
                  r'+7(\1)\2-\3-\4', digits)


def normalize_name(name) -> str:
    return re.sub(r'\s+', ' ', name).strip()


def normalize_amount(amount) -> float:
    return float(amount.replace(' ', '').replace(',', '.'))


def normalize_data(data, normalizers) -> list:
    for line in data:
        for key, value in line.items():
            # Применяем функцию нормализации,
            # если она существует для текущего ключа
            normalize_func = normalizers.get(key, lambda x: x)
            line[key] = normalize_func(value)
    return data

normalizers = {
    'phone': normalize_phone,
    'fullname': normalize_name,
    'some_amount': normalize_amount
}