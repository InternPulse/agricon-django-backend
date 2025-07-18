import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
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

def send_welcome_email(to_email: str):
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

    from_email = 'agriconteam@gmail.com'
    to_email = To(to_email)
    subject = "Welcome to Agricon Nigeria!"

    plain_text_content = (
    "Welcome to Agricon\n\n"
    "Hi There,\n\n"
    "You’re now part of AgriCon — where farmers and facility owners connect to reduce post-harvest losses.\n\n"
    "What’s next?\n"
    "- 🔍 Book nearby drying, cold, or processing facilities\n"
    "- 🏢 List your own facility\n"
    "- 📱 Access AgriCon on web\n\n"
    "Thanks for signing up. We're here to help you and your team. If you have any questions, contact us at hello@agricon.com.\n\n"
    "Open Agricon: https://agricon.com.ng\n"
    )
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Welcome to Agricon</title>
    </head>
    <body style="margin:0; padding:0; background-color:#F7F7F7; font-family: Arial, sans-serif;">

    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-height: 100vh; background-color:#F7F7F7; padding: 32px 16px;">
        <tr>
        <td align="center">

            <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color:#ffffff; border-radius:32px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 32px;">
            <tr>
                <td align="left">
                <img src="https://github.com/InternPulse/agricon-frontend/blob/main/src/assets/agriconLogo.png?raw=true" alt="Agricon logo" width="120" style="display: block; height: auto; border: 0;" />
                </td>
            </tr>

            <tr>
                <td style="padding-top: 32px; font-size: 24px; font-weight: 600; line-height: 1.2; color: #000000;">
                Welcome to Agricon
                </td>
            </tr>

            <tr>
                <td style="padding-top: 16px; font-size: 16px; font-weight: 400; line-height: 1.3; color: #000000;">
                Hi {to_email},
                </td>
            </tr>

            <tr>
                <td style="padding-top: 12px; font-size: 16px; font-weight: 400; line-height: 1.3; color: #000000;">
                You’re now part of AgriCon — where farmers and facility owners connect to reduce post-harvest losses.
                </td>
            </tr>

            <tr>
                <td style="padding-top: 24px; font-size: 16px; font-weight: 500; color: #000000;">
                What’s next?
                </td>
            </tr>

            <tr>
                <td style="padding-top: 8px; padding-left: 24px; font-size: 16px; line-height: 1.5; color: #000000;">
                <ul style="margin: 0; padding-left: 18px;">
                    <li>🔍 Book nearby drying, cold, or processing facilities</li>
                    <li>🏢 List your own facility</li>
                    <li>📱 Access AgriCon on web</li>
                </ul>
                </td>
            </tr>

            <tr>
                <td style="padding-top: 24px; font-size: 16px; font-weight: 400; line-height: 1.4; color: #000000;">
                Thanks for signing up. We're here to help you and your team. If you have any questions, contact us at
                <a href="mailto:hello@agricon.com" style="color: #02402D; text-decoration: underline;">hello@agricon.com</a>.
                </td>
            </tr>

            <tr>
                <td align="center" style="padding-top: 32px;">
                <a href="https://agricon.com.ng" target="_blank" style="
                    background-color: #02402D;
                    color: #ffffff;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 16px;
                    line-height: 1;
                    padding: 14px 48px;
                    border-radius: 9999px;
                    display: inline-block;
                    min-width: 173px;
                    text-align: center;
                    cursor: pointer;
                ">
                    Open Agricon
                </a>
                </td>
            </tr>
            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """

    content = Content("text/plain", plain_text_content)
    mail = Mail(from_email, to_email, subject, content)
    mail.add_content(Content("text/html", html_content))

    try:
        response = sg.send(mail)
        # Optional: log or handle response.status_code if needed
    except Exception as e:
        print(f"Error sending welcome email: {e}")