def postprocess_text(data):
    """
    Преобразует вложенный список строк в одну строку с элементами,
    заключёнными в кавычки и разделёнными запятыми

    :param data: json файл
    :return: Строка, содержащая все элементы из вложенных списков
    """
    return '\n'.join(line for block in data["results"] for line in block), data["work_url"]
