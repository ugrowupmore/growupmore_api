# utils/utils.py

import random

def generate_otp(length=6):
    """
    Generates a random OTP of specified length.
    
    :param length: Length of the OTP (default is 6)
    :return: A string representing the OTP
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
