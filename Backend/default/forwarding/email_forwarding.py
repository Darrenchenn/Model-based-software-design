import configparser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from default.common import error

config = configparser.ConfigParser()
config.read(os.getcwd() + '/config.ini')
sender_email = config.get('smtp', 'sender_email')
smtp_server = config.get('smtp', 'host')
smtp_port = config.get('smtp', 'port')
smtp_username = config.get('smtp', 'username')
smtp_password = config.get('smtp', 'password')
smtp_protocol = config.get('smtp', 'protocol')


def forward_email(recipient_email: str, subject: str, message: str):
    if not sender_email or \
        not smtp_server or \
            not smtp_port or \
                not smtp_username or \
                    not smtp_password or \
                        not smtp_protocol:
        return error.Error("Invalid SMTP configuration")
    if not recipient_email or \
        not subject or \
            not message:
        return error.Error("Invalid email parameters")
    try:
        
        # Choose to use SSL or TLS
        if smtp_protocol == "TLS":
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
        elif smtp_protocol == "SSL":
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            return error.Error("Invalid SMTP protocol")

        # Log in to your SMTP server using your username and password
        server.login(smtp_username, smtp_password)

        # Create a MIMEText object to represent the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the email message
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Close the SMTP server session
        server.quit()
        
        return "Email forwarded successfully"
    
    except Exception as e:
        return error.Error(f"Failed to forward email, error: {str(e)}")



# Example usage:
recipient_email = ""
subject = "Forwarded Email Subject"
message = "This is the forwarded email content."
result = forward_email(recipient_email, subject, message)
print(result)