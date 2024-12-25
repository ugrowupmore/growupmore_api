# utils/email_utils.py

import logging
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import strip_tags

# Initialize logger
logger = logging.getLogger('authuser')  # Use the appropriate logger

def send_custom_email(subject, html_content, recipient_list, from_email=None, fail_silently=False):
    
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    plain_message = strip_tags(html_content)
    email = EmailMessage(
        subject=subject,
        body=html_content,  # Use HTML content directly
        from_email=from_email,
        to=recipient_list,
    )
    email.content_subtype = "html"

    try:
        email.send(fail_silently=fail_silently)
        logger.info(f"Email sent successfully to {', '.join(recipient_list)} with subject '{subject}'.")
    except Exception as e:
        logger.error(f"Failed to send email to {', '.join(recipient_list)} with subject '{subject}': {str(e)}", exc_info=True)
        if not fail_silently:
            raise e
