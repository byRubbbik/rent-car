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
            count = 0
            for i in regform["password"]:
                count += 1
            if count >= 8:
                user = register(regform)
                return user
            else:
                return 1
    return False
    
            