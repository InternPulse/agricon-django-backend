from django.core.mail import send_mail

def send_otp_email(to_email, otp_code):
    subject = 'Your AgriCon Email OTP'
    message = f'Your OTP code is: {otp_code}\n\nThis code will expire in 5 minutes.'
    from_email = None  # Will use DEFAULT_FROM_EMAIL
    html_message = f"""
        <p>Hello,</p>
        <p>Your <strong>OTP code</strong> is: <code>{otp_code}</code></p>
        <p>This code will expire in 5 minutes.</p>
        <p>– AgriCon Team</p>
    """
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
