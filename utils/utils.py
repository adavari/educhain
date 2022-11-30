import random
import string


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + '0123456789@'
    return ''.join(random.choice(letters) for i in range(string_length))
