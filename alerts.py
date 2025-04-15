import logging
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
import os

def send_email_alert(subject, body):
    if os.getenv("EMAIL_ENABLED") != "true":
        return
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv("FROM_EMAIL")
    msg['To'] = os.getenv("TO_EMAIL")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv("FROM_EMAIL"), os.getenv("APP_PASSWORD"))
            server.send_message(msg)
    except Exception as e:
        logging.error(f"Email failed: {e}")

def send_sms_alert(body):
    if os.getenv("SMS_ENABLED") != "true":
        return
    try:
        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
        client.messages.create(body=body, from_=os.getenv("FROM_PHONE"), to=os.getenv("TO_PHONE"))
    except Exception as e:
        logging.error(f"SMS failed: {e}")