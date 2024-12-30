# utils/sms_otp_utils.py

import requests
import logging
from django.conf import settings

# Initialize logger
logger = logging.getLogger('authuser')  # Use the appropriate logger

def send_otp_sms(destination, otp_code, campaign_name="otp_verification"):
    """
    Sends an SMS using the provided API.

    :param destination: The recipient's mobile number with country code (e.g., +919662278990)
    :param otp_code: The OTP code to send
    :param campaign_name: The campaign name for the SMS (default: "otp_verification")
    :return: Boolean indicating if the SMS was sent successfully
    """
    url = "https://backend.aisensy.com/campaign/t1/api/v2"
    payload = {
        "apiKey": settings.SMS_API_KEY,
        "campaignName": campaign_name,
        "destination": destination,
        "userName": "Grow Up More",
        "source": "organic",
        "templateParams": [
            otp_code
        ],
        "buttons": [
            {
                "type": "button",
                "sub_type": "url",
                "index": "0",
                "parameters": [
                    {
                        "type": "text",
                        "text": otp_code
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info(f"SMS sent successfully to {destination} with OTP {otp_code}.")
            return True
        else:
            logger.error(f"Failed to send SMS to {destination}. Status Code: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception occurred while sending SMS to {destination}: {str(e)}", exc_info=True)
        return False
