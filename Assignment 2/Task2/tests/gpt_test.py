import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
from online_shopping_cart.checkout import checkout_process # Replace with the actual module name

# Sample test data
global_products = [
    MagicMock(name="Product1", units=5, get_product_unit=lambda: {"name": "Product1", "price": 10}),
    MagicMock(name="Product2", units=0, get_product_unit=lambda: {"name": "Product2", "price": 15}),
]
global_cart = MagicMock()
sample_user_data = [
    {"username": "test_user", "wallet": 100},
    {"username": "another_user", "wallet": 50},
]

@pytest.fixture
def mock_globals():
    """Fixture to mock global variables."""
    with patch('checkout_process.global_products', global_products), \
         patch('checkout_process.global_cart', global_cart):
        yield

@pytest.fixture
def mock_file_io():
    """Fixture to mock file I/O."""
    mock_file_data = json.dumps(sample_user_data)
    with patch('checkout_process.open', mock_open(read_data=mock_file_data)) as mock_file, \
         patch('json.dump') as mock_json_dump:
        yield mock_file, mock_json_dump

@pytest.fixture
def mock_user_interface():
    """Fixture to mock user input and output."""
    with patch('checkout_process.UserInterface.get_user_input') as mock_input, \
         patch('builtins.print') as mock_print:
        yield mock_input, mock_print

@pytest.fixture
def login_info():
    """Fixture for sample login info."""
    return {"username": "test_user", "wallet": 100}

def test_checkout_and_payment_display_products(mock_globals, mock_user_interface, login_info):
    """Test displaying products."""
    mock_input, mock_print = mock_user_interface
    mock_input.side_effect = ['d', 'l']  # Simulate displaying products and logging out

    checkout_process.checkout_and_payment(login_info)

    mock_print.assert_any_call('Displaying products available for purchase...')  # Replace with actual expected message
    mock_print.assert_any_call('Invalid input. Please try again.')

def test_checkout_and_payment_check_cart(mock_globals, mock_file_io, mock_user_interface, login_info):
    """Test checking the cart."""
    mock_input, mock_print = mock_user_interface
    mock_file, mock_json_dump = mock_file_io
    global_cart.check_cart.return_value = True

    mock_input.side_effect = ['c', 'l']  # Simulate checking the cart and logging out

    checkout_process.checkout_and_payment(login_info)

    mock_json_dump.assert_called_once()  # Verify wallet update in users.json
    mock_print.assert_any_call('Cart checked successfully.')  # Replace with expected cart message

def test_checkout_and_payment_add_to_cart(mock_globals, mock_user_interface, login_info):
    """Test adding a product to the cart."""
    mock_input, mock_print = mock_user_interface
    mock_input.side_effect = ['1', 'l']  # Simulate selecting a product and logging out

    checkout_process.checkout_and_payment(login_info)

    global_cart.add_item.assert_called_once_with(global_products[0].get_product_unit())
    mock_print.assert_any_call(f'{global_products[0].name} added to your cart.')

def test_checkout_and_payment_logout(mock_globals, mock_user_interface, login_info):
    """Test logging out."""
    mock_input, mock_print = mock_user_interface
    mock_input.side_effect = ['l']  # Simulate logging out

    with patch('checkout_process.exit') as mock_exit:
        checkout_process.checkout_and_payment(login_info)

        mock_exit.assert_called_once_with(0)

def test_checkout_and_payment_invalid_input(mock_globals, mock_user_interface, login_info):
    """Test invalid input."""
    mock_input, mock_print = mock_user_interface
    mock_input.side_effect = ['x', 'l']  # Simulate invalid input and logging out

    checkout_process.checkout_and_payment(login_info)

    mock_print.assert_any_call('Invalid input. Please try again.')
