import random
import string

ALPHABET = string.ascii_letters + string.digits


# Пока так =)
def generate_api_key() -> str:
    return "".join([random.choice(ALPHABET) for _ in range(16)])
