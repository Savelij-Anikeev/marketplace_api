import uuid


class UserService:

    @staticmethod
    def generate_username() -> str:
        magic = "".join(str(uuid.uuid4()).split('-'))[:-12:2]
        login = '@user' + '-' + magic

        return login
