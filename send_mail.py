import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message, to_email, smtp_server, smtp_port, smtp_user, smtp_password):
    """
    Function to send an email using SMTP protocol.

    Args:
        subject (str): The subject of the email.
        message (str): The body message of the email.
        to_email (str): The recipient email address.
        smtp_server (str): The SMTP server address.
        smtp_port (int): The SMTP server port.
        smtp_user (str): The SMTP server username.
        smtp_password (str): The SMTP server password or app password.

    Returns:
        None
    """
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(message, 'plain'))

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            # Log in to the SMTP server
            server.login(smtp_user, smtp_password)
            
            # Send email
            server.sendmail(smtp_user, to_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage:
# subject = "Test Email"
# message = "This is a test email sent from Python."
# to_email = "abburisahithi33@gmail.com"
# smtp_server = "smtp.gmail.com"
# smtp_port = 465
# smtp_user = "hermoinegrangerjean79@gmail.com"
# smtp_password = "onxt ubyi sbaa kbyt"  # Use App Password for Gmail

# send_email(subject, message, to_email, smtp_server, smtp_port, smtp_user, smtp_password)
