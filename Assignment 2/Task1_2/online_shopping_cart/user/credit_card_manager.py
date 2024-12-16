from online_shopping_cart.user.user_data import UserDataManager

class CreditCardManager:
    @staticmethod
    def add_credit_card(user, is_new_user = False):
        """Add a new credit card to the user's profile."""
        card_number = input("Enter card number: ").strip()
        expiry_date = input("Enter expiry date (MM/YY): ").strip()
        card_name = input("Enter name on card: ").strip()
        cvc = input("Enter CVC: ").strip()

        user.credit_cards.append({
            'card_number': card_number,
            'expiry_date': expiry_date,
            'card_name': card_name,
            'cvv': cvc
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
        index = int(input("Enter the number of the card to edit: ")) - 1
        if 0 <= index < len(user.credit_cards):
            print("Enter new details for the card:")
            card_number = input("Enter new card number: ").strip()
            expiry_date = input("Enter new expiry date (MM/YY): ").strip()
            card_name = input("Enter new name on card: ").strip()
            cvv = input("Enter new CVV: ").strip()

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
