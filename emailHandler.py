import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, sender, recipients, password):
    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipients
    msg['Subject'] = subject

    # Attach the message to the MIME object
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Login to the SMTP server
    server.login(sender, password)

    # Send the email
    server.sendmail(sender, recipients, msg.as_string())

    # Quit the SMTP server
    server.quit()
