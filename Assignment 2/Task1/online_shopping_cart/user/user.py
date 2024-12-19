################
# USER CLASSES #
################


class User:

    def __init__(self, name, wallet, credit_cards) -> None:
        self.name: str = name
        self.wallet: float = wallet
        self.credit_cards: list[dict[str, str]] = credit_cards  # List to store CC details