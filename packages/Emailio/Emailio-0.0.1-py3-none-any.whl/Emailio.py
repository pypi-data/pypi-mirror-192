import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from datetime import datetime


class Emailio:
    def send_email_with_attachment(self, host, port, sender_email, password, receiver_emails, file_path,subject=None,body_text=None):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_emails)
        current_time = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        msg['Subject'] = subject

        if os.path.isfile(file_path):
            body = body_text
            filename = os.path.basename(file_path)
            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)
        else:
            body = "Attachment not Found"

        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        print("Email sent!")
        server.quit()
