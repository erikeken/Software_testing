from online_shopping_cart.user.user_data import UserDataManager
from online_shopping_cart.user.user_interface import UserInterface

class CreditCardManager:
    @staticmethod
    def add_credit_card(user, is_new_user = False):
        """Add a new credit card to the user's profile."""
        card_number = UserInterface.get_user_input(prompt="Enter card number: ").strip()
        expiry_date = UserInterface.get_user_input(prompt="Enter expiry date (MM/YY): ").strip()
        card_name = UserInterface.get_user_input(prompt="Enter name on card: ").strip()
        cvv = UserInterface.get_user_input(prompt="Enter CVV: ").strip()

        user.credit_cards.append({
            'card_number': card_number,
            'expiry_date': expiry_date,
            'card_name': card_name,
            'cvv': cvv
        })

        if is_new_user:
            return

        UserDataManager.update_user_data(user)

    @staticmethod
    def edit_credit_card(user):
        """Edit an existing credit card."""
        if not user.credit_cards:
            print("No credit cards available to edit.")
            return

        CreditCardManager.list_credit_cards(user)
        index = int(UserInterface.get_user_input(prompt="Enter the number of the card to edit: ")) - 1
        if 0 <= index < len(user.credit_cards):
            print("Enter new details for the card:")
            card_number = UserInterface.get_user_input(prompt="Enter new card number: ").strip()
            expiry_date = UserInterface.get_user_input(prompt="Enter new expiry date (MM/YY): ").strip()
            card_name = UserInterface.get_user_input(prompt="Enter new name on card: ").strip()
            cvv = UserInterface.get_user_input(prompt="Enter new CVV: ").strip()

            user.credit_cards[index] = {
                'card_number': card_number,
                'expiry_date': expiry_date,
                'card_name': card_name,
                'cvv': cvv
            }
            UserDataManager.update_user_data(user)
            print("Credit card updated successfully.")
        else:
            print("Invalid selection.")

    @staticmethod
    def list_credit_cards(user):
        """List all credit cards associated with the user."""
        if not user.credit_cards:
            print("No credit cards available.")
        else:
            print("Credit cards:")
            for i, card in enumerate(user.credit_cards, 1):
                print(f"{i}. {card['card_name']} - {card['card_number'][-4:]} (Expires: {card['expiry_date']})")
