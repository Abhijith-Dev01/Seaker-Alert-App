import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_email(recipient: list, subject: str, body: str):
    load_dotenv()
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")    
    smtp_port = int(os.getenv("SMTP_PORT"))                       

    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = " ,".join(recipient)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        # print("Email sent!")
    except Exception as e:
        return f"Failed to send email: {e}"