from django.core.mail import EmailMessage
from django.conf import settings
from threading import Thread
from django.utils.html import format_html

def send_custom_email(subject, body, to_emails, attachments=None):
    def send():
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_emails
        )
        email.send(fail_silently=False)
        print("Mail send successfully")
    Thread(target=send).start()

def send_custom_html_email(subject, html, to_emails, attachments=None):
    def send():
        html_content = format_html(html)
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_emails
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        print("Mail send successfully")
    Thread(target=send).start()
    
    # email = EmailMessage(
    #     subject=subject,
    #     body=body,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to=to_emails
    # )

    # if attachments:
    #     for attachment in attachments:
    #         email.attach_file(attachment)

    # email.send(fail_silently=False)

# def send_custom_email(subject, body, to_emails, attachments=None):
#     if attachments:
#         for attachment in attachments:
            # email.attach_file(attachment)
