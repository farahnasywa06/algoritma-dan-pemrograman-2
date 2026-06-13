class User:

    def __init__(
        self,
        username: str,
        password: str,
        email: str
    ):

        self.username = username
        self.password = password
        self.email = email

    def to_dict(self):

        return {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }

    @classmethod
    def from_dict(
        cls,
        data
    ):

        return cls(
            username=data["username"],
            password=data["password"],
            email=data["email"]
        )
