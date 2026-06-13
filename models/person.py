class Person:
    def __init__(self, full_name, email, phone):
        self._full_name = full_name
        self._email = email
        self._phone = phone

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    def profile_summary(self):
        return f"{self.full_name} - {self.email}"
