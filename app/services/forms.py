# Обработка форм
from app.services.auth import auth, register


def login_forms(loginform):
    if loginform:
        user = auth(loginform)
        return user
    return False


def reg_forms(regform):
    if regform["username"]:
        if regform["password"]:
            user = register(regform)
            return user
    return False
    
            