###############################
# USER AUTHENTICATION CLASSES #
###############################
import re # using the re module for password verification

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
            'wallet': 0.0,
            'credit_cards': []  # Initialize with an empty list of credit cards
        }

        # Prompt for credit card details
        while True:
            add_card = input("Would you like to add a credit card now? (y/n): ").strip().lower()
            if add_card == 'y':
                card_details = UserAuthenticator.get_credit_card_details()
                new_user['credit_cards'].append(card_details)
            elif add_card == 'n':
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        data.append(new_user)
        UserDataManager.save_users(data)  # Rewrite the file with the added user

    @staticmethod
    def get_credit_card_details():
        """Prompt for credit card details and return as a dictionary."""
        card_number = input("Enter card number: ").strip()
        expiry_date = input("Enter expiry date (MM/YY): ").strip()
        card_name = input("Enter name on card: ").strip()
        cvv = input("Enter CVV: ").strip()

        return {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'card_name': card_name,
            'cvv': cvv
        }

    @staticmethod
    def edit_credit_card_details(username, data):
        """Allow users to edit their credit card details."""
        user = next((u for u in data if u['username'].lower() == username.lower()), None)
        if not user:
            print("User not found.")
            return

        if not user['credit_cards']:
            print("No credit cards found.")
            return

        print("Current credit cards:")
        for idx, card in enumerate(user['credit_cards'], start=1):
            print(f"{idx}. {card['card_name']} ({card['card_number'][-4:]})")

        card_idx = int(input("Enter the number of the card to edit: ")) - 1
        if 0 <= card_idx < len(user['credit_cards']):
            user['credit_cards'][card_idx] = UserAuthenticator.get_credit_card_details()
            UserDataManager.save_users(data)
            print("Credit card details updated.")
        else:
            print("Invalid selection.")
