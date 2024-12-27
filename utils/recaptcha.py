# authapp/utils/recaptcha.py

import requests
from django.conf import settings

def validate_recaptcha(token):
    """
    Validates the reCAPTCHA token with Google's API.
    
    :param token: The reCAPTCHA token sent by the client.
    :return: Boolean indicating if the token is valid.
    """
    secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
    data = {
        'secret': secret_key,
        'response': token
    }
    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()
        return result.get('success', False) and result.get('score', 0) >= 0.5
    except Exception:
        # Log the exception if needed
        return False
