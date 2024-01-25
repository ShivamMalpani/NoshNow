from enum import Enum

class OrderStatus(Enum):
    ACTIVE = 'active'
    FREEZED = 'freezed'
    CANCELLED = 'cancelled'


class OrderType(Enum):
    INSTANT = 'instant'
    STUDENT = 'student'
    SLOT = 'slot'
    STUDENT_SLOT = 'student_slot'


class PaymentStatus(Enum):
    PAID = 'paid'
    NOT_PAID = 'not_paid'


class PaymentType(Enum):
    WALLET = 'wallet'
    COD = 'cod'
    UPI = 'upi'


class Address(Enum):
    KANHAR = 'kanhar'
    INDRAVATI = 'indravati'
    SHIVNATH = 'shivnath'