import smtplib # This will be used to send emails to the restockers
from email.mime.text import MIMEText

def send_instructions():
    pass # This function will send out the instructions out to a restocker



    subject = input("Subject: ")
    body = input("Body: ")
    sender = "sender@gmail.com"
    recipients = ["recipient1@gmail.com", "recipient2@gmail.com"]
    password = "password"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")