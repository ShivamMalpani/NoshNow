from enum import Enum

class OrderStatus(Enum):
    ACTIVE = 'active'
    FREEZED = 'freezed'
    CANCELLED = 'cancelled'
    DELIVERED = 'delivered'
    DELIVERED_PERSON_REACHED = 'deliveryPersonReached'
    IN_TRANSIT = 'inTransit'
    PENDING_ACCEPTANCE = 'pending_acceptance'


class OrderType(Enum):
    INSTANT = 'instant'
    STUDENT = 'student'
    SLOT = 'slot'
    STUDENT_SLOT = 'student_slot'


class PaymentStatus(Enum):
    PAID = 'paid'
    NOT_PAID = 'not_paid'
    REFUND = 'refund'


class PaymentType(Enum):
    WALLET = 'wallet'
    COD = 'cod'
    UPI = 'upi'


class Address(Enum):
    KANHAR = 'kanhar'
    INDRAVATI = 'indravati'
    SHIVNATH = 'shivnath'


class PaymentReason(Enum):
    ORDER_CANCELLATION = 'order_cancellation'
    ORDER_PLACE = 'order_place'


class UserType(Enum):
    STUDENT = 'student'
    RESTAURANT = 'restaurant'
    DRIVER = 'driver'