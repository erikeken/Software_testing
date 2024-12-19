from itertools import product

import pytest
from pytest import fixture

from online_shopping_cart.checkout.checkout_process import checkout_and_payment, checkout
from online_shopping_cart.product.product import Product
from online_shopping_cart.user.user_login import login, register_user
from online_shopping_cart.user.user import User
from online_shopping_cart.user.user_authentication import UserAuthenticator
from online_shopping_cart.user.credit_card_manager import CreditCardManager

class TestCheckout:

    @pytest.fixture
    def cart_stub(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.ShoppingCart')

    @pytest.fixture
    def login_stub1(self):
        return {'username': 'Samantha', 'wallet': 148.0}

    @pytest.fixture
    def login_stub2(self):
        return {'username': 'Samantha', 'wallet': 0.0}

    @pytest.fixture
    def login_stub3(self):
        return {'username': 'Samantha', 'wallet': 0.2}

    @pytest.fixture
    def display_products_available_for_purchase_stub(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.display_products_available_for_purchase')

    @pytest.fixture
    def logout_stub(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)

    @pytest.fixture
    def logout_stub1(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.logout', side_effect=[False, True])

    @pytest.fixture
    def check_cart_stub1(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.check_cart', return_value=True)

    @pytest.fixture
    def check_cart_stub2(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.check_cart', return_value=False)



    # test the display branch
    def test_checkout_and_payment3(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                   display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect= ["d", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        display_products_available_for_purchase_stub.assert_called_once()



    # test normal check out cart
    def test_checkout_and_payment6(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                   check_cart_stub1):
        mock_data = [{"username": "Ramanathan","password": "Notaproblem23*","wallet": 100.0},
                     {"username": "Samantha","password": "SecurePass123/^","wallet": 150.0}]
        mock_file = mocker.mock_open()
        mocker.patch('builtins.open', mock_file)
        mock_load = mocker.patch("json.load", return_value=mock_data)
        mock_dump = mocker.patch("json.dump")
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=["c", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        check_cart_stub1.assert_called_once()
        mock_load.assert_called_once()
        mock_dump.assert_called_once_with([{"username": "Ramanathan","password": "Notaproblem23*","wallet": 100.0},
                                           {"username": "Samantha","password": "SecurePass123/^","wallet": 148.0}],
                                          mock_file.return_value, indent=2)

    # test check out cart edge case with 0 in wallet
    def test_checkout_and_payment7(self, cart_stub, login_stub2, mocker, monkeypatch, capsys,
                                   check_cart_stub1):
        mock_data = [{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100.0},
                     {"username": "Samantha", "password": "SecurePass123/^", "wallet": 150.0}]
        mock_file = mocker.mock_open()
        mocker.patch('builtins.open', mock_file)
        mock_load = mocker.patch("json.load", return_value=mock_data)
        mock_dump = mocker.patch("json.dump")
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["c", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub2)

        captured = capsys.readouterr()
        check_cart_stub1.assert_called_once()
        mock_load.assert_called_once()
        mock_dump.assert_called_once_with(
            [{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100.0},
             {"username": "Samantha", "password": "SecurePass123/^", "wallet": 0.0}],
            mock_file.return_value, indent=2)


    # test item out of stock
    def test_checkout_and_payment19(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["1", "1", "1", "l"])
        mock_product = [Product('Tomato', 1, 2)]
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', mock_product)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch.object(cart_stub, "add_item")
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert cart_stub.add_item.call_count == 2
        assert (captured.out == 'Tomato added to your cart.\nTomato added to your cart.\nSorry, Tomato is out of stock.\n')

    # test empty product list
    def test_checkout_and_payment20(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["1", "l"])
        mock_product = []
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', mock_product)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch.object(cart_stub, "add_item")
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert cart_stub.add_item.call_count == 0
        assert (captured.out == 'Invalid input. Please try again.\n')


    @fixture
    def mock_user_data(self, mocker):
        """Fixture to mock user data."""
        return mocker.patch('online_shopping_cart.user.user_data.UserDataManager.load_users', return_value=[
            {'username': 'testuser', 'password': 'Test@1234', 'wallet': 50.0},
            {'username': 'user\with\special', 'password': 'Pass@5678', 'wallet': 100.0},
            {'username': 'user3', 'password': 'Hello@7890', 'wallet': 200.0}
        ])

    @fixture
    def mock_save_users(self, mocker):
        """Fixture to mock saving user data."""
        return mocker.patch('online_shopping_cart.user.user_data.UserDataManager.save_users')

    @fixture
    def mock_user_input(self, mocker):
        """Fixture to mock user input."""
        return mocker.patch('online_shopping_cart.user.user_interface.UserInterface.get_user_input')

    @fixture
    def mock_cart_empty(self, mocker):
        """Fixture to create a mock cart that is empty."""
        cart = mocker.Mock()
        cart.is_empty.return_value = True
        cart.retrieve_items.return_value = []
        return cart

    @fixture
    def mock_cart_with_items(self, mocker):
        """Fixture to create a mock cart with items."""
        cart = mocker.Mock()
        cart.is_empty.return_value = False
        cart.retrieve_items.return_value = ["Cheese", "Onion", "Strawberry"]
        return cart

    def test_login_success(self, mock_user_data, mock_user_input):
        """Test successful login."""
        mock_user_input.side_effect = ['testuser', 'Test@1234']

        result = login()

        expected_output = {'username': 'testuser', 'wallet': 50.0}

        for key, value in expected_output.items():
            assert result[key] == value

    def test_login_invalid_credentials(self, mock_user_data, mock_user_input, capsys):
        """Test login with invalid credentials."""
        mock_user_input.side_effect = ['testuser', 'WrongPassword','n']
        result = login()
        captured = capsys.readouterr()
        assert result is None, "Login should return None for invalid credentials"
        assert "Login failed." in captured.out, "Expected failure message not found in output"

    def test_login_user_not_found_register(self, mock_user_data, mock_save_users, mock_user_input):
        """Test login when user is not found and chooses to register."""
        mock_user_input.side_effect = [
            'newuser',  # Username
            'weeeeee', # random input(stupid code)
            'y',  # Register prompt
            'New@User1',  # Password
            'n'
        ]

        login()

        # Validate the arguments passed to save_users
        saved_data = mock_save_users.call_args[0][0]
        new_user = next((user for user in saved_data if user['username'] == 'newuser'), None)

        assert new_user is not None
        assert new_user['password'] == 'New@User1'
        assert new_user['wallet'] == 0.0

    def test_login_after_registering_new_user(self, mock_user_data, mock_save_users, mock_user_input, capsys):
        """Regression test for login immediately after registering a new user."""
        mock_user_input.side_effect = [
            'newuser',  # Username not found
            '11111',  # Random invalid input (ignored)
            'y',  # Prompt to register
            'New@User1',  # Password during registration
            'n',  # Add credit card prompt (skipped if exists)
            'newuser',  # Attempt login
            'New@User1'  # Valid password
        ]

        # Run the first login attempt, leading to registration
        result = login()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assert the registration message was printed
        assert "Congratulations newuser! you are now registered!" in captured.out

        # Run the second login attempt, verifying the user can log in
        result2 = login()

        # Capture the printed output again
        captured2 = capsys.readouterr()
        assert "Successfully logged in." in captured2.out

        # Validate the login result
        expected_output = {'username': 'newuser', 'wallet': 0.0}

        for key, value in expected_output.items():
            assert result2[key] == value

    def test_login_empty_username(self, mock_user_data, mock_save_users, mock_user_input, capsys):
        """Test login when username is empty."""
        mock_user_input.side_effect = [
            '',  # Empty username input
            'qqq',
            'y', # Register prompt
            'Test@1234',  # Any password
            'n'
        ]

        # Run the login function
        result = login()

        # Capture printed output
        captured = capsys.readouterr()

        # Verify if the system handled empty username appropriately
        assert result is None, "Login should not proceed with empty username"
        assert "Congratulations ! you are now registered! Try login in" in captured.out, "broken"

################################### After creditcard implementation tests ########################################


    def test_checkout_with_credit_card_payment(self, mocker, mock_user_input, mock_cart_with_items):
        user = User(name="Erik", wallet=10.0, credit_cards=[
            {'card_number': "4111111111111111", 'expiry_date': "12/25", 'card_name': "John's Card", 'cvv': "123"}
        ])
        mock_cart_with_items.get_total_price.return_value = 50.0  # Mock total price
        mock_cart_with_items.clear_items = mocker.Mock()

        mock_user_input.side_effect=[
            "card", "1"
        ]

        checkout(user, mock_cart_with_items)


    def test_checkout_add_credit_card(self, mocker, mock_cart_with_items):
        user = User(name="Erik", wallet=0.0, credit_cards=[])
        mock_cart_with_items.get_total_price.return_value = 50.0  # Mock total price
        mock_cart_with_items.clear_items = mocker.Mock()

        mocker.patch('builtins.input', side_effect=[
            "card",  # Payment method
            "y",     # Add a credit card
            "4111111111111111", "12/25", "Erik's New Card", "123",  # Card details
            "1"      # Select the newly added card
        ])

        checkout(user, mock_cart_with_items)

        assert len(user.credit_cards) == 1, "A new credit card should be added."
        mock_cart_with_items.clear_items.assert_called_once()

    def test_edit_credit_card(self, mock_user_input):
        """Test editing an existing credit card."""
        # Mock user with existing credit cards
        user = User(
            name="Erik",
            wallet=100.0,
            credit_cards=[
                {'card_number': "4111111111111111", 'expiry_date': "12/25", 'card_name': "newuser", 'cvv': "123"}
            ]
        )

        mock_user_input.side_effect=[
            "1",  # First card
            "4222222222222222",  # New card number
            "01/26",  # New expiry date
            "neweruser",  # New name
            "456"  # New CVV
        ]

        CreditCardManager.edit_credit_card(user)

        assert len(user.credit_cards) == 1, "There should still be one credit card."
        assert user.credit_cards[0]['card_number'] == "4222222222222222", "Card number was not updated correctly."
        assert user.credit_cards[0]['expiry_date'] == "01/26", "Expiry date was not updated correctly."
        assert user.credit_cards[0]['card_name'] == "neweruser", "Card name was not updated correctly."
        assert user.credit_cards[0]['cvv'] == "456", "CVV was not updated correctly."

    ######################### LOGIN TESTS ############################

    def test_register_with_credit_card(self, mocker, mock_user_input):
        data = []
        mock_user_input.side_effect=[
            "y",  # Add credit card
            "4111111111111111", "12/25", "newuser", "123", "n"  # Card details
        ]

        UserAuthenticator.register("newuser", "New@User1", data)

        assert len(data) == 1, "User data should include one new user."
        assert len(data[0]['credit_cards']) == 1, "Credit card should be added during registration."
        assert data[0]['credit_cards'][0]['card_name'] == "newuser", "Credit card name mismatch."

    def test_register_without_credit_card(self, mock_user_input):
        """Test user registration without adding a credit card."""
        data = []

        mock_user_input.side_effect=[
            "n"  # Do not add an credit card
        ]
        UserAuthenticator.register("newuser", "New@User1", data)

        assert len(data) == 1, "User data should include one new user."
        assert data[0]['credit_cards'] == [], "No credit cards should be added."

    def test_register_with_multiple_credit_cards(self, mock_user_input):
        """Test user registration with multiple credit cards."""
        data = []

        mock_user_input.side_effect=[
            "y",  # Add first card
            "4111111111111111", "12/25", "newuser", "123",  # First card details
            "y",  # Add second card
            "4222222222222222", "01/26", "neweruser", "456",  # Second card details
            "n"  # Stop
        ]

        UserAuthenticator.register("newuser", "New@User1", data)

        assert len(data) == 1, "User data should include one new user."
        assert len(data[0]['credit_cards']) == 2, "Two credit cards should be added during registration."

        # assert first card
        assert data[0]['credit_cards'][0]['card_number'] == "4111111111111111", "First card number mismatch."
        assert data[0]['credit_cards'][0]['expiry_date'] == "12/25", "First card expiry date mismatch."
        assert data[0]['credit_cards'][0]['card_name'] == "newuser", "First card name mismatch."
        assert data[0]['credit_cards'][0]['cvv'] == "123", "First card CVV mismatch."

        # second card
        assert data[0]['credit_cards'][1]['card_number'] == "4222222222222222", "Second card number mismatch."
        assert data[0]['credit_cards'][1]['expiry_date'] == "01/26", "Second card expiry date mismatch."
        assert data[0]['credit_cards'][1]['card_name'] == "neweruser", "Second card name mismatch."
        assert data[0]['credit_cards'][1]['cvv'] == "456", "Second card CVV mismatch."
