from django.contrib.auth import get_user_model

# Получаем модель пользователя из Django
User = get_user_model()


def create_user(username, password, email, **kwargs):
    """
    Создает обычного пользователя.
    :param username: Имя пользователя
    :param password: Пароль пользователя
    :param email: Email пользователя
    :param kwargs: Дополнительные поля (например, first_name, last_name)
    :return: Созданный пользователь
    """
    # Создаем пользователя с указанными данными
    user = User.objects.create(
        username=username,
        email=email,
        **kwargs
    )
    # Устанавливаем пароль в безопасном формате
    user.set_password(password)
    user.save()
    return user


def create_superuser(username, password, email):
    """
    Создает суперпользователя.
    :param username: Имя суперпользователя
    :param password: Пароль суперпользователя
    :param email: Email суперпользователя
    :return: Созданный суперпользователь
    """
    # Создаем суперпользователя с указанными данными
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    return user


def get_admin_user():
    """
    Возвращает существующего суперпользователя или создает нового, если его нет.
    :return: Суперпользователь
    """
    try:
        # Пытаемся найти суперпользователя по имени пользователя
        return User.objects.get(username="admin", is_superuser=True)
    except User.DoesNotExist:
        # Если суперпользователь не найден, создаем нового
        return create_superuser(
            username="admin",
            password="Admin1",
            email="Admin1@mail.ru"
        )


def create_member_user(username, password, email):
    """
    Создает обычного пользователя-участника.
    :param username: Имя пользователя
    :param password: Пароль пользователя
    :param email: Email пользователя
    :return: Созданный пользователь
    """
    # Вызываем функцию create_user для создания участника
    return create_user(username=username, password=password, email=email)


def get_member_user():
    """
    Возвращает тестового пользователя-участника или создает нового, если его нет.
    :return: Пользователь-участник
    """
    try:
        # Пытаемся найти тестового пользователя по имени пользователя
        return User.objects.get(username="test1")
    except User.DoesNotExist:
        # Если пользователь не найден, создаем нового
        user = User.objects.create(
            username="test1",
            email="test1@mail.ru",
        )
        user.set_password('test1')
        user.save()
        return user
