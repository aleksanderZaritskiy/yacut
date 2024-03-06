class NotValidCustomId(Exception):
    """Вызывается при невалидном custom_id"""

    pass


class DublicateCustomId(Exception):
    """Вызывается когда пользователь
    ввел custom_id уже существующий в базе
    """

    pass


class MaxIterationDept(Exception):
    """Возникает когда все возможные
    варианты коротких ссылок уже существуют
    """

    pass
