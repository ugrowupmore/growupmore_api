# utils/email_utils.py

from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import strip_tags

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
    email.send(fail_silently=fail_silently)
