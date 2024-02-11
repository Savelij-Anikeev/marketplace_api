import uuid


class UserService:

    @staticmethod
    def generate_username(first_name: str, last_name: str) -> str:
        magic = "".join(str(uuid.uuid4()).split('-'))[:-12:2]
        login = '@' + first_name + '-' + last_name + '-' + magic

        return login
