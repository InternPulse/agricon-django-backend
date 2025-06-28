import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

logger = logging.getLogger(__name__)

def send_otp_email(to_email, otp_code):
    subject = 'Your AgriCon Email OTP'
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <title>AgriCon OTP</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #F7F7F7; padding: 20px; text-align: center;">
        <div style="max-width: 600px; margin: auto; background-color: #fff; border-radius: 20px; padding: 40px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            
            <img src="https://github.com/InternPulse/agricon-frontend/blob/main/src/assets/agriconLogo.png?raw=true" alt="Agricon logo" style="width: 120px; height: auto;" />
            
            <h2 style="margin-top: 30px;">Verify Your Email – AgriCon One-Time Password (OTP)</h2>

            <p>Hi {to_email},</p>
            <p>Your AgriCon OTP is:</p>

            <div style="margin: 20px 0;">
            <span style="display: inline-block; padding: 12px 24px; background-color: #475367; color: #fff; font-size: 20px; border-radius: 4px; letter-spacing: 4px;">
                {otp_code}
            </span>
            </div>

            <p>This code will expire in 10 minutes.</p>
            <p>Please enter this code in the app to continue setting up your account.</p>

            <hr style="margin: 40px 0;">

            <p><strong>Need Help?</strong></p>
            <p>If you didn’t request this, please ignore this email.</p>
            <p>For support, contact us at <a href="mailto:support@agricon.ng">support@agricon.ng</a></p>

            <hr style="margin: 40px 0;">

            <p><strong>AgriCon Nigeria</strong></p>
            <p>Connecting Farmers to Shared Infrastructure</p>
            <p>&copy; 2025 AgriCon. All rights reserved.</p>

        </div>
        </body>
        </html>
        """


    message = Mail(
        from_email='agriconteam@gmail.com',  # ✅ Must be a verified sender in SendGrid
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logger.info(f"Email sent to {to_email}. Status: {response.status_code}")
    except Exception as e:
        logger.error(f"SendGrid email failed for {to_email}: {str(e)}")
