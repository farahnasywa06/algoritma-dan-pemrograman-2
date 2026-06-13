from models.person import Person


class Student(Person):
    def __init__(
        self,
        nim: str,
        full_name: str,
        major: str,
        year: int,
        gpa: float,
        email: str,
        phone: str,
    ):
        super().__init__(full_name, email, phone)

        # Encapsulation
        self.__nim = nim
        self.__major = major
        self.__year = year
        self.__gpa = gpa

    @property
    def nim(self):
        return self.__nim

    @property
    def major(self):
        return self.__major

    @major.setter
    def major(self, value):
        self.__major = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        self.__gpa = value

    def profile_summary(self):
        """
        Polymorphism
        override method parent
        """
        return f"{self.nim} | {self.full_name} | {self.major}"

    def to_dict(self):
        return {
            "nim": self.nim,
            "full_name": self.full_name,
            "major": self.major,
            "year": self.year,
            "gpa": self.gpa,
            "email": self.email,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nim=data["nim"],
            full_name=data["full_name"],
            major=data["major"],
            year=int(data["year"]),
            gpa=float(data["gpa"]),
            email=data["email"],
            phone=data["phone"],
        )
