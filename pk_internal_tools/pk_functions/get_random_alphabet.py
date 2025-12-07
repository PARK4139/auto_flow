

def get_random_alphabet():
    import random
    import string

    # logging.debug(f"{inspect.currentframe().f_code.co_name}()")
    return random.choice(string.ascii_letters)
