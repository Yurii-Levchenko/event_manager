from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

User = get_user_model()
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=instance.email,
            subject="Welcome to WeMeet!",
            html_content=f"<strong>Hi {instance.name},</strong><br><br>"
                         f"Thank you for registering at ! We are excited to have you on board. Let's meet today!"
        )
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(f"Email sent: {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")

