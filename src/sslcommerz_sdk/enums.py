from enum import Enum


class Choices(Enum):
    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == str(other)

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def get_choices(cls):
        return [(choice.value, choice.name) for choice in cls]


class TransactionStatus(Choices):
    INVALID = "INVALID"
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    # IPN notification status
    VALID = "VALID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    UNATTEMPTED = "UNATTEMPTED"
    EXPIRED = "EXPIRED"
