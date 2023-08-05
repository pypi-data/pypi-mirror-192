import random

def generate(first_name: str, last_name: str, numbers=True):
    first_name = first_name.lower()
    last_name = last_name.lower()
    username_string = ""
    username_string += first_name[:2]
    username_string += last_name[:2]
    username_string += random.choice(first_name)
    if numbers:
        random_numbers = [str(random.randint(0, 9)) for _ in range(3)]
        random_numbers_string = "".join(random_numbers)
        username_string += random_numbers_string
    return username_string
