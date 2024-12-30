import random
import string

from app.core.security import get_password_hash


def random_lower_string(amount: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=amount))


def random_email() -> str:
    return f"{random_lower_string(10)}@{random_lower_string(5)}.com"


def random_password() -> str:
    return get_password_hash(random_lower_string(8))


def random_int(min: int = 1, max: int = 100) -> int:
    return random.randint(min, max)


def random_bool() -> bool:
    return bool(random.getrandbits(1))