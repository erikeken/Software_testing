###############################
# USER AUTHENTICATION CLASSES #
###############################
from online_shopping_cart.user.user_data import UserDataManager


class PasswordValidator:

    @staticmethod
    def is_valid(password) -> bool:
        pass  # TODO: Task 1: validate password for registration


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
    def register(username, password, data) -> None: # register new user, needs username, password and the current user list
        new_user = {
            'username': username,
            'password': password,
            'wallet': 0.0
        }
        data.append(new_user) # append the new user to user list
        UserDataManager.save_users(data) # rewrite the .json with the added user
        pass  # TODO: Task 1: register username and password as new user to file with 0.0 wallet funds
