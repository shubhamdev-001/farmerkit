

import random
from django.core.mail import send_mail
from django.conf import settings
from farmerkit.settings import EMAIL_HOST_USER

def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    """Send OTP to user via email"""
    subject = 'Your OTP for Login'
    message = f'Your OTP for login is: {otp}. This OTP is valid for 5 minutes.'
    from_email = EMAIL_HOST_USER
    recipient_list = [email
        ]
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"OTP sent to {email}: {otp}")
        return True
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return False