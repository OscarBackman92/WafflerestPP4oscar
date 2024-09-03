from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_confirmation_mail(subject, recipient_list, context, template_name):
    """
    Send an email with the given subject, recipient list, and context.
    Uses the specified template for the email content.
    """
    # Render the HTML content and plain text content
    html_content = render_to_string(template_name, context)
    plain_content = strip_tags(html_content)

    # Send email
    send_mail(
        subject,
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
        html_message=html_content
    )
