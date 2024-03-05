class NotValidCustomId(Exception):
    """Вызывается при невалидном custom_id"""

    pass


class DublicateCustomId(Exception):
    """Вызывается когда пользователь
    ввел custom_id уже существующий в базе
    """

    pass
