import string
from app.models import User

abc = string.ascii_letters + string.digits + '_'


def validate_password(password, return_all=False):
    errors = set()
    if not (8 <= len(password) <= 30):
        error = 'Длина пароля должна быть от 8 до 30 символов'
        if not return_all:
            return error
        errors.add(error)
    contains_upper, contains_lower, contains_digit = False, False, False
    for letter in password:
        if letter not in abc:
            error = 'Недопустимые символы. Пароль должен состоять только из латинских букв цифр и символа нижнего подчеркивания'
            if not return_all:
                return error
            errors.add(error)
        if letter.islower():
            contains_lower = True
        elif letter.isupper():
            contains_upper = True
        elif letter.isdigit():
            contains_digit = True
    if not (contains_upper and contains_lower and contains_digit):
        error = 'Пароль должен содержать как минимум 1 заглавную букву, одну строчную и одну цифру'
        if not return_all:
            return error
        errors.add(error)
    return list(errors) if len(errors) else None


def validate_username(username, return_all=False):
    errors = set()
    if User.objects.filter(username=username).count():
        error = 'Имя пользователя занято'
        if not return_all:
            return error
        errors.add(error)
    if not (5 <= len(username) <= 20):
        error = 'Длина пароля должная быть от 5 до 20 символов'
        if not return_all:
            return error
        errors.add(error)
    for letter in username:
        if letter not in abc:
            error = 'Недопустимые символы. Логин должен состоять только из латинских букв цифр и символа нижнего подчеркивания'
            if not return_all:
                return error
            errors.add(error)
    return list(errors) if len(errors) else None
