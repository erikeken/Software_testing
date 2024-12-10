from pytest import fixture
from unittest.mock import MagicMock
from online_shopping_cart.user.user_authentication import UserAuthenticator
from online_shopping_cart.user.user_interface import UserInterface
from online_shopping_cart.user.user_data import UserDataManager
from online_shopping_cart.user.user_logout import logout
from online_shopping_cart.user.user_login import login, register_user


class TestUserAuthentication:

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
        assert result == {'username': 'testuser', 'wallet': 50.0}

    def test_login_invalid_credentials(self, mock_user_data, mock_user_input, capsys):
        """Test login with invalid credentials."""
        mock_user_input.side_effect = ['testuser', 'WrongPassword','n']
        result = login()
        captured = capsys.readouterr()
        assert result is None, "Login should return None for invalid credentials"
        assert "Login failed." in captured.out, "Expected failure message not found in output"

    def test_register_duplicate_username(self, mock_user_data, mock_save_users, mock_user_input, capsys):
        """Test registration with a duplicate username."""
        mock_user_input.side_effect = [
            'testuser',  # Duplicate username
            'Valid@Pass123'  # Valid password
        ]

        # Attempt to register the duplicate username
        register_user('testuser', data=mock_user_data.return_value)

        # Capture printed output
        captured = capsys.readouterr()
        assert "Congratulations testuser! you are now registered! Try login in" in captured.out

        # Ensure save_users was not called
        mock_save_users.assert_called_once()

    def test_login_user_not_found_register(self, mock_user_data, mock_save_users, mock_user_input):
        """Test login when user is not found and chooses to register."""
        mock_user_input.side_effect = [
            'newuser',  # Username
            'weeeeee', # random input(stupid code)
            'y',  # Register prompt
            'New@User1'  # Password
        ]

        login()

        # Validate the arguments passed to save_users
        saved_data = mock_save_users.call_args[0][0]
        new_user = next((user for user in saved_data if user['username'] == 'newuser'), None)

        assert new_user is not None
        assert new_user['password'] == 'New@User1'
        assert new_user['wallet'] == 0.0

    def test_login_empty_username(self, mock_user_data, mock_save_users, mock_user_input, capsys):
        """Test login when username is empty."""
        mock_user_input.side_effect = [
            '',  # Empty username input
            'qqq',
            'y', # Register prompt
            'Test@1234'  # Any password
        ]

        # Run the login function
        result = login()

        # Capture printed output
        captured = capsys.readouterr()

        # Verify if the system handled empty username appropriately
        assert result is None, "Login should not proceed with empty username"
        assert "Congratulations ! you are now registered! Try login in" in captured.out, "broken"


    def test_register_password_validation(self, mock_save_users, mock_user_input):
        """Test password validation during registration."""
        mock_user_input.side_effect = [
            'newuser',       # Username
            'doesnotwork',      # Invalid password
            'doesnot@work',      # Invalid password
            'Doesnotwork123456789',      # invalid password
            'Valid@Pass123'  # Valid password
        ]

        mock_data = []
        register_user('newuser', data=mock_data)

        # Verify if save_users was called
        mock_save_users.assert_called_once()
        saved_data = mock_save_users.call_args[0][0]
        new_user = next((user for user in saved_data if user['username'] == 'newuser'), None)

        # Validate new user
        assert new_user is not None
        assert new_user['password'] == 'Valid@Pass123'
        assert new_user['wallet'] == 0.0

    def test_login_after_registering_new_user(self, mock_user_data, mock_save_users, mock_user_input, capsys):
        """Test login immediately after registering a new user."""
        mock_user_input.side_effect = [
            'newuser',  # Username not found
            '11111',
            'y',
            'New@User1', # Password during registration
            'newuser',  # Attempt login
            'New@User1'  # Valid password
        ]
        # Run the login function
        result = login()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assert the relevant message was printed
        assert "Congratulations newuser! you are now registered!" in captured.out
        result2 = login()
        captured2 = capsys.readouterr()
        assert "Successfully logged in." in captured2.out
        # Validate the login result
        assert result2 == {'username': 'newuser', 'wallet': 0.0}

    def test_login_empty_password(self, mock_user_data, mock_user_input, capsys):
        """Test login fails if password is empty."""

        mock_user_input.side_effect = [
            'testuser',  # Username input
            '',  # Empty password input
            'n'
        ]

        result = login()
        captured = capsys.readouterr()
        assert result is None  # Since the login should fail
        assert "Login failed." in captured.out  # Ensure failure message

    def test_login_special_characters_in_username(self, mock_user_data, mock_user_input):
        """Test login works with special characters in username."""
        mock_user_input.side_effect = ['user\\with\\special', 'Pass@5678']

        result = login()

        assert result == {'username': 'user\\with\\special', 'wallet': 100.0}

    def test_login_password_with_spaces(self, mock_user_data, mock_user_input):
        """Test login fails if password contains leading or trailing spaces."""
        mock_user_input.side_effect = ['testuser', ' Test@1234 ','n']  # Password with spaces

        result = login()

        assert result is None

######################### Logout tests ###################################
    def test_logout_empty_cart(self, mock_cart_empty, mock_user_input, capsys):
        """Test logout when cart is empty."""
        mock_user_input.return_value = 'y'

        result = logout(mock_cart_empty)

        # Assert result is True
        assert result is True

        # Assert cart.is_empty() was called
        mock_cart_empty.is_empty.assert_called_once()

        # Assert cart.retrieve_items() was NOT called
        mock_cart_empty.retrieve_items.assert_not_called()

        # Capture and assert printed output
        captured = capsys.readouterr()
        assert "Your cart is not empty." not in captured.out
        assert "You have been logged out." in captured.out


    def test_logout_with_items_confirm(self, mock_cart_with_items, mock_user_input, capsys):
        """Test logout when cart has items and user confirms logout."""
        mock_user_input.return_value = 'y'

        result = logout(mock_cart_with_items)

        # Assert result is True
        assert result is True

        # Assert cart methods are called
        mock_cart_with_items.is_empty.assert_called_once()
        mock_cart_with_items.retrieve_items.assert_called_once()

        # Capture and assert printed output
        captured = capsys.readouterr()
        assert "Your cart is not empty." in captured.out
        assert "Cheese" in captured.out
        assert "Onion" in captured.out
        assert "Strawberry" in captured.out
        assert "You have been logged out." in captured.out

    def test_logout_with_items_cancel(self, mock_cart_with_items, mock_user_input, capsys):
        """Test logout when cart has items and user cancels logout."""
        mock_user_input.return_value = 'n'

        result = logout(mock_cart_with_items)

        # Assert result is False
        assert result is False

        # Assert cart methods are called
        mock_cart_with_items.is_empty.assert_called_once()
        mock_cart_with_items.retrieve_items.assert_called_once()

        # Capture and assert printed output
        captured = capsys.readouterr()
        assert "Your cart is not empty." in captured.out
        assert "Cheese" in captured.out
        assert "Onion" in captured.out
        assert "Strawberry" in captured.out

        # Check if logged out
        assert "You have been logged out." not in captured.out

    def test_logout_confirm_mixed_case(self, mock_cart_empty, mock_user_input, capsys):
        """Test logout with mixed case input for confirmation."""
        mock_user_input.return_value = 'Y'

        result = logout(mock_cart_empty)

        # Assert logout is successful
        assert result is True

        # Capture printed output
        captured = capsys.readouterr()
        assert "You have been logged out." in captured.out

    def test_logout_reject_mixed_case(self, mock_cart_empty, mock_user_input, capsys):
        """Test rejecting logout with mixed case input."""
        mock_user_input.return_value = 'N'  # Mixed case rejection

        result = logout(mock_cart_empty)

        # Assert logout is canceled
        assert result is False

        captured = capsys.readouterr()
        assert "You have been logged out." not in captured.out

    def test_logout_large_cart(self, mock_user_input, mocker, capsys):
        """Test logout when the cart has a large number of items."""
        large_cart = mocker.Mock() # create a fake carts with 100 items to see if the system can handle many items
        large_cart.is_empty.return_value = False
        large_cart.retrieve_items.return_value = [f"Item{i}" for i in range(100)]  # 100 items
        mock_user_input.return_value = 'y'

        result = logout(large_cart)

        # Assert logout is successful
        assert result is True

        captured = capsys.readouterr()
        assert "Your cart is not empty. You have the following items:" in captured.out
        assert "Item0" in captured.out
        assert "Item99" in captured.out
        assert "You have been logged out." in captured.out

    def test_logout_invalid_input(self, mock_cart_empty, mock_user_input, capsys):
        """Test logout when user provides invalid input."""
        mock_user_input.side_effect = ['invalid']  # Invalid input

        result = logout(mock_cart_empty)

        # Assert logout is unsuccessful
        assert result is not True

        # Capture printed output
        captured = capsys.readouterr()
        assert "You have been logged out." not in captured.out, "Should not log out"

    def test_cancel_logout_empty_cart(self, mock_cart_empty, mock_user_input, capsys):
        """Test canceling logout when the cart is empty."""
        mock_user_input.return_value = 'n'

        result = logout(mock_cart_empty)
        assert result is False
        captured = capsys.readouterr()
        assert "You have been logged out." not in captured.out

    def test_logout_no_confirmation_input(self, mock_cart_empty, mock_user_input):
        """Test logout when the user does not provide confirmation."""
        mock_user_input.side_effect = ['']
        result = logout(mock_cart_empty)
        # Assert logout is unsuccessful
        assert result is False

    def test_logout_special_characters_input(self, mock_cart_empty, mock_user_input):
        """Test logout when the user provides special characters as input."""
        mock_user_input.side_effect = ['@@@']  # Special character input

        result = logout(mock_cart_empty)
        assert result is not True

