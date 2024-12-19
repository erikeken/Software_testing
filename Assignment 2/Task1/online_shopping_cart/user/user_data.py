import json

################################
# USER DATA MANAGEMENT CLASSES #
################################


class UserDataManager:

    USER_FILE_PATHNAME: str = './files/users.json'

    @staticmethod
    def load_users() -> list[dict[str, str | float | list[dict[str, str]]]]:
        try:
            with open(file=UserDataManager.USER_FILE_PATHNAME, mode='r') as file:
                return json.load(fp=file)
        except FileNotFoundError:
            print('File not found.')
            exit(1)

    @staticmethod
    def save_users(data: list[dict[str, str | float | list[dict[str, str]]]]) -> None:
        with open(file=UserDataManager.USER_FILE_PATHNAME, mode='w') as file:
            json.dump(obj=data, fp=file, indent=2)


    @staticmethod
    def update_user_data(user):
        """
        Update the user's data in the JSON file.
        """
        data = UserDataManager.load_users()
        for entry in data:
            if entry['username'] == user.name:
                # Update the user's data in memory
                entry['wallet'] = user.wallet
                entry['credit_cards'] = user.credit_cards
                break
        else:
            print(f"User {user.name} not found in the data file.")

        # Save the updated data back to the JSON file
        UserDataManager.save_users(data)