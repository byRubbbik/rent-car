# Обработка форм
from app.services.auth import auth, register, add_user_info


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


def user_info_forms(userinfoForms):
    if userinfoForms['first_name'] and userinfoForms['last_name']:
        if userinfoForms['phone_number'] and userinfoForms['email']:
            return add_user_info(userinfoForms)
    return False
