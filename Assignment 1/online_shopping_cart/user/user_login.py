from online_shopping_cart.user import user_data
from online_shopping_cart.user.user_authentication import UserAuthenticator, PasswordValidator
from online_shopping_cart.user.user_interface import UserInterface
from online_shopping_cart.user.user_data import UserDataManager

########################
# USER LOGIN FUNCTIONS #
########################

def is_quit(input_argument: str) -> bool:
    return input_argument.lower() == 'q'

def register_user(username: str, data) -> None:
    """Prompts the user to input username and password, registers user if the password meets the criteria(special, upper and length) if not prompt again"""
    while True:
        password = UserInterface.get_user_input(prompt='Enter a password: ')

        if PasswordValidator.is_valid(password):
            UserAuthenticator.register(username=username, password=password, data=data)
            print('Congratulations! you are now registered! Try login in')
            break
        else:
            print('Password must have at least 8 characters, one special character and one upper case character. Try again')

def login() -> dict[str, str | float] | None:
    username: str = UserInterface.get_user_input(prompt="Enter your username (or 'q' to quit): ")
    if is_quit(input_argument=username):
        exit(0)  # The user has quit

    password: str = UserInterface.get_user_input(prompt="Enter your password (or 'q' to quit): ")
    if is_quit(input_argument=password):
        exit(0)   # The user has quit

    is_authentic_user: dict[str, str | float] = UserAuthenticator().login(
        username=username,
        password=password,
        data=UserDataManager.load_users()
    )
    if is_authentic_user is not None:
        return is_authentic_user

    # TODO: Task 1: prompt user to register when not found

    # Prompt user to register if username is not found
    register_prompt = UserInterface.get_user_input(f"Username '{username}' not found. Would you like to register? (y/n): ")
    if register_prompt.lower() == 'y':
        register_user(username, data=UserDataManager.load_users())

    return None
