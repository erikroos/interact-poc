import string
import random

def generate_code(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))