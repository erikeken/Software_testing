import pytest
from pytest_mock import mocker

from online_shopping_cart.checkout.checkout_process import checkout_and_payment, checkout
from online_shopping_cart.product.product import Product


class TestCheckout:

    @pytest.fixture
    def cart_stub(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.ShoppingCart')

    @pytest.fixture
    def user_stub(self, mocker):
        return mocker.patch('online_shopping_cart.checkout.checkout_process.User')

    @pytest.fixture
    def login_stub1(self):
        return {'username': 'Samantha', 'wallet': 148.0}

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
    # v102,v108,v109,v114,v126,v127,v128
    def test_checkout_and_payment1(self, cart_stub, login_stub1, mocker, monkeypatch, capsys, logout_stub):
        mocker.patch("online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect= ["l"])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_products', [['Tomato', '1', '15']])
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_cart', cart_stub)
        mocker.patch('online_shopping_cart.checkout.checkout_process.global_user_file_path', "tests/users.json")
        mocker.patch('builtins.exit')

        checkout_and_payment(login_stub1)

        captured = capsys.readouterr()
        logout_stub.assert_called_once()

    # test not logging out the first time
    # v108,v109,v114,v126,v127,v108
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
    # v102,v108,v109,v113
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

    # test not check out cart
    # v108,v109,v114,v115,v108
    def test_checkout_and_payment4(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
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
    # v102,v108,v109,v114,v115,v119,v120,v121,v122
    # v120,v121,v122,v120
    def test_checkout_and_payment5(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
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

    # invalid letter input
    # v102,v108,v109,v114,v126,v130,v138
    def test_checkout_and_payment6(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
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

    # test add one item to cart
    # v102,v108,v109,v114,v126,v130,v131,v133
    def test_checkout_and_payment7(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
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

    # test item out of stock
    # v102,v108,v109,v114,v126,v130,v131,v136
    def test_checkout_and_payment8(self, cart_stub, login_stub1, mocker, monkeypatch, capsys,
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

    # test normal check out
    # v31,v35,v39
    def test_checkout9(self, cart_stub, user_stub, mocker, monkeypatch, capsys):
        mocker.patch.object(cart_stub, "get_total_price", return_value=18)
        mocker.patch.object(cart_stub, "items", return_value=[Product('Tomato', 18, 1)])
        mocker.patch.object(cart_stub, "clear_items", return_value=None)
        mocker.patch.object(user_stub, "wallet", 148)

        checkout(user_stub, cart_stub)

        captured = capsys.readouterr()
        assert cart_stub.get_total_price.call_count == 1
        assert user_stub.wallet == 130
        assert cart_stub.clear_items.call_count == 1
