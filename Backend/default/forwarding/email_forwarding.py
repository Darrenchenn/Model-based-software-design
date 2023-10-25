import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from default.common import error

# SMTP server settings
sender_email = ""
smtp_server = "smtp.example.com"
smtp_username = ""
smtp_password = ""
smtp_protocol = "TLS"  # Choose between SSL or TLS

def forward_email(recipient_email: str, subject: str, message: str):
    try:
        # Choose to use SSL or TLS
        if smtp_protocol == "TLS":
            server = smtplib.SMTP(smtp_server, port=587)
            server.starttls()  # 启用 TLS 加密
        elif smtp_protocol == "SSL":
            server = smtplib.SMTP_SSL(smtp_server, port=465)
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
        return f"Failed to forward email, error: {str(e)}"

# Example usage:
recipient_email = ""
subject = "Forwarded Email Subject"
message = "This is the forwarded email content."
result = forward_email(recipient_email, subject, message)
print(result)