"""Data classes: Person (abstract) -> Student, Warden, plus Room, Visitor, Complaint."""
from abc import ABC, abstractmethod
from datetime import datetime
from exceptions import InvalidInputError


class Person(ABC):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    @abstractmethod
    def get_role(self):
        """Every child class MUST write this method."""

    def get_info(self):
        return f"{self.name} ({self.phone})"

    def __str__(self):
        return self.get_info()

    @staticmethod
    def is_valid_phone(phone):
        return phone.isdigit() and len(phone) == 10


class Student(Person):
    TOTAL_FEE = 50000                       # class variable: same for all students

    def __init__(self, student_id, name, phone, course, room_no, fee_paid=0):
        super().__init__(name, phone)
        self.student_id = student_id
        self.course = course
        self.room_no = room_no
        self.__fee_paid = fee_paid          # private variable

    def get_role(self):                     # overriding the abstract method
        return "Student"

    def get_info(self):                     # overriding the parent method (polymorphism)
        return f"Student {self.name} | {self.course} | Room {self.room_no} | Fee due {self.get_fee_due()}"

    def get_fee_paid(self):
        return self.__fee_paid

    def get_fee_due(self):
        return Student.TOTAL_FEE - self.__fee_paid

    def pay_fee(self, amount):
        if amount <= 0:
            raise InvalidInputError("Amount must be greater than 0")
        if amount > self.get_fee_due():
            raise InvalidInputError("Amount is more than the due fee")
        self.__fee_paid += amount

    def to_dict(self):
        return {"student_id": self.student_id, "name": self.name, "phone": self.phone,
                "course": self.course, "room_no": self.room_no, "fee_paid": self.__fee_paid}


class Warden(Person):
    def __init__(self, warden_id, name, phone, block):
        super().__init__(name, phone)
        self.warden_id = warden_id
        self.block = block

    def get_role(self):
        return "Warden"

    def get_info(self):                     # different output from Student.get_info()
        return f"Warden {self.name} | Block {self.block} | Phone {self.phone}"

    def to_dict(self):
        return {"warden_id": self.warden_id, "name": self.name,
                "phone": self.phone, "block": self.block}


class Room:
    def __init__(self, room_no, capacity):
        self.room_no = room_no
        self.capacity = capacity
        self.occupants = []                 # list of student ids

    def is_full(self):
        return len(self.occupants) >= self.capacity

    def vacancies(self):
        return self.capacity - len(self.occupants)


class Visitor:
    def __init__(self, student_id, name, time_in, time_out=""):
        self.student_id = student_id
        self.name = name
        self.time_in = time_in
        self.time_out = time_out

    def to_dict(self):
        return self.__dict__.copy()         # all attributes as a dictionary


class Complaint:
    def __init__(self, student_id, text, date, status="Open"):
        self.student_id = student_id
        self.text = text
        self.date = date
        self.status = status

    def to_dict(self):
        return self.__dict__.copy()


def now_text():
    return datetime.now().strftime("%d-%m-%Y %H:%M")
