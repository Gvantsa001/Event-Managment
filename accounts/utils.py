from django.core.mail import EmailMessage
import random
from django.conf import settings
from .models import User, OneTimePassword
from django.contrib.sites.shortcuts import get_current_site


def send_generated_otp_to_mail(email, request):
    subject = "One time Passcode for email verification"
    otp = random.randint(1000,9999)
    current_site = get_current_site(request).domain
    user = User.objects.get(email=email)
    email_body = f"Hi {user.first_name} thanks for sign up on {current_site}, please verify your email with following code\n Code"
    from_email = settings.EMAIL_HOST
    otp_obj = OneTimePassword.objects.create(user=user, otp=otp)

    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[user.email])
    d_email.send()

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]

    )

    email.send()