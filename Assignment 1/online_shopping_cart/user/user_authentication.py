###############################
# USER AUTHENTICATION CLASSES #
###############################
import re # using the re module for password verification

from online_shopping_cart.user.user_data import UserDataManager


class PasswordValidator:

    @staticmethod
    def is_valid(password) -> bool:
        check_upper = any(i.isupper() for i in password)
        check_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
        check_length = len(password) >= 8

        if check_upper or check_special or check_length:
            return True
        else:
            return False
          # TODO: Task 1: validate password for registration


class UserAuthenticator:

    @staticmethod
    def login(username, password, data) -> dict[str, str | float] | None:
        is_user_registered: bool = False

        for entry in data:
            if entry['username'].lower() == username.lower():
                is_user_registered = True
            if is_user_registered:
                if entry['password'].lower() == password.lower():
                    print('Successfully logged in.')
                    return {
                        'username': entry['username'],
                        'wallet': entry['wallet']
                    }
                break

        if not is_user_registered:
            print('User is not registered.')
        else:
            print('Login failed.')
        return None

    @staticmethod
    def register(username, password, data) -> None:
        new_user = {
            'username': username,
            'password': password,
            'wallet': 0.0
        }
        data.append(new_user)
        UserDataManager.save_users(data)
          # TODO: Task 1: register username and password as new user to file with 0.0 wallet funds
