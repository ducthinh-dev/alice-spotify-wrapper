import string
import random


def generate_random_string(length: str) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
