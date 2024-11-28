from itertools import product

import pytest
from pytest_mock import mocker

from online_shopping_cart.checkout.checkout_process import checkout_and_payment
from online_shopping_cart.product.product import Product


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


    # test logout
    def test_checkout_and_payment1(self, cart_stub, login_stub1, mocker, monkeypatch, capsys, logout_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect= ["l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        logout_stub.assert_called_once()

    # test not logging out the first time and then attempts log out again
    def test_checkout_and_payment2(self, cart_stub, login_stub1, mocker, monkeypatch, capsys, logout_stub1):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=["l", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert logout_stub1.call_count == 2

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

    # test the display branch with line break in the input
    def test_checkout_and_payment4(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                   display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["d\nc", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mock_logout = mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        display_products_available_for_purchase_stub.assert_called_once()
        mock_logout.assert_called_once()

    # test not check out cart
    def test_checkout_and_payment5(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                   check_cart_stub2):
        mock_data = [{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100.0},
                     {"username": "Samantha", "password": "SecurePass123/^", "wallet": 150.0}]
        mock_file = mocker.mock_open()
        mock_open = mocker.patch('builtins.open', mock_file)
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=["c", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        check_cart_stub2.assert_called_once()
        mock_open.assert_not_called()

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

    # test check out cart edge case with float in wallet
    def test_checkout_and_payment8(self, cart_stub, login_stub3, mocker, monkeypatch, capsys,
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

        checkout_and_payment(login_stub3)

        captured = capsys.readouterr()
        check_cart_stub1.assert_called_once()
        mock_load.assert_called_once()
        mock_dump.assert_called_once_with(
            [{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100.0},
             {"username": "Samantha", "password": "SecurePass123/^", "wallet": 0.2}],
            mock_file.return_value, indent=2)

    # invalid letter input
    def test_checkout_and_payment9(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                   display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["g\tsdf", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert (captured.out == 'Invalid input. Please try again.\n')

    # invalid float input
    def test_checkout_and_payment10(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                   display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["23.65", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert (captured.out == 'Invalid input. Please try again.\n')

    # invalid base 16 input
    def test_checkout_and_payment11(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["\x01", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert (captured.out == 'Invalid input. Please try again.\n')

    # invalid blank space input
    def test_checkout_and_payment12(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["     ", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert (captured.out == 'Invalid input. Please try again.\n')

    # invalid list input
    def test_checkout_and_payment13(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                   display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["[c]", "l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert (captured.out == 'Invalid input. Please try again.\n')

    # test product number above boundary edge case
    def test_checkout_and_payment14(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["525", "l"])
        mock_product = [Product('Tomato', 1, 15)]
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', mock_product)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert (captured.out == 'Invalid input. Please try again.\n')

    # test product number below boundary edge case
    def test_checkout_and_payment15(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["0", "l"])
        mock_product = [Product('Tomato', 1, 15)]
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', mock_product)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert (captured.out == 'Invalid input. Please try again.\n')

    # test add one item to cart
    def test_checkout_and_payment16(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["1", "l"])
        mock_product = [Product('Tomato', 1, 15)]
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', mock_product)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch.object(cart_stub, "add_item")
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        cart_stub.add_item.assert_called_once()
        assert (captured.out == 'Tomato added to your cart.\n')

    # test add multiple of the same items to cart
    def test_checkout_and_payment17(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["1", "1", "1", "l"])
        mock_product = [Product('Tomato', 1, 15)]
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', mock_product)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch.object(cart_stub, "add_item")
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert cart_stub.add_item.call_count == 3
        assert (captured.out == 'Tomato added to your cart.\nTomato added to your cart.\nTomato added to your cart.\n')

    # test add different items to cart
    def test_checkout_and_payment18(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
                                    display_products_available_for_purchase_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input",
                     side_effect=["1", "1", "2", "l"])
        product1 = Product('Tomato', 1, 15)
        product2 = Product('Onion', 0.8, 20)
        mock_product = [product1, product2 ]
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', mock_product)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch.object(cart_stub, "add_item")
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('online_shopping_cart.checkout.checkout_process.logout', return_value=True)
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        assert cart_stub.add_item.call_count == 3
        assert (captured.out == 'Tomato added to your cart.\nTomato added to your cart.\nOnion added to your cart.\n')

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
