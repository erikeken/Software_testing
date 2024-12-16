###############################
# USER AUTHENTICATION CLASSES #
###############################
import re # using the re module for password verification
from online_shopping_cart.user.credit_card_manager import CreditCardManager
from online_shopping_cart.user.user import User
from online_shopping_cart.user.user_data import UserDataManager


class PasswordValidator:

    @staticmethod
    def is_valid(password) -> bool:
        check_upper = any(i.isupper() for i in password) # check if the password contains one or more upper letter
        check_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)) # check if password contains any special characters
        check_length = len(password) >= 8 #check if length is equal or more than 8 characters

        return check_upper and check_special and check_length # If all =true return true else false
            #return True
        #else:
#            return False
          # Task 1: validate password for registration


class UserAuthenticator:

    @staticmethod
    def login(username, password, data) -> dict[str, str | float | list[dict[str, str]]] | None:
        is_user_registered: bool = False

        for entry in data:
            if entry['username'].lower() == username.lower():
                is_user_registered = True
            if is_user_registered:
                if entry['password'].lower() == password.lower():
                    print('Successfully logged in.')
                    return {
                        'username': entry['username'],
                        'wallet': entry['wallet'],
                        'credit_cards': entry['credit_cards']
                    }
                break

        if not is_user_registered:
            print('User is not registered.')
        else:
            print('Login failed.')
        return None

    @staticmethod
    def register(username, password, data) -> None:
        # Create a new User object with username and wallet initialized to 0.0
        new_user = User(name=username, wallet=0.0, credit_cards=[])

        # Prompt for credit card details
        while True:
            add_card = input("Would you like to add a credit card now? (y/n): ").strip().lower()
            if add_card == 'y':
                CreditCardManager.add_credit_card(new_user, is_new_user=True)
            elif add_card == 'n':
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        # Convert the new User object to a dictionary and append to data
        user_data = {
            'username': new_user.name,
            'password': password,
            'wallet': new_user.wallet,
            'credit_cards': new_user.credit_cards
        }
        data.append(user_data)

        # Save updated data to the storage
        UserDataManager.save_users(data)