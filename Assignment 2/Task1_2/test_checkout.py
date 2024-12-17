from itertools import product

import pytest
from pytest import fixture

from online_shopping_cart.checkout.checkout_process import checkout_and_payment
from online_shopping_cart.product.product import Product
from online_shopping_cart.user.user_login import login, register_user



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