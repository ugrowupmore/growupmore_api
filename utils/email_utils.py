# utils/email_utils.py

import logging
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialize logger
logger = logging.getLogger('authuser')  # Use the appropriate logger

def send_custom_email(subject, html_content, recipient_list, from_email=None, fail_silently=False):
    """
    Sends a custom email using SendGrid.

    :param subject: Subject of the email
    :param html_content: HTML content of the email
    :param recipient_list: List of recipient email addresses
    :param from_email: Sender's email address (optional)
    :param fail_silently: If True, suppress exceptions
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # Create a Mail object
    message = Mail(
        from_email=from_email,
        to_emails=recipient_list,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(
            f"Email sent successfully to {', '.join(recipient_list)} with subject '{subject}'. "
            f"Status Code: {response.status_code}"
        )
    except Exception as e:
        logger.error(
            f"Failed to send email to {', '.join(recipient_list)} with subject '{subject}': {str(e)}",
            exc_info=True
        )
        if not fail_silently:
            raise e

