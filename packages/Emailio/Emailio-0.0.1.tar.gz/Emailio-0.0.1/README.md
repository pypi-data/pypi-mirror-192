# Emailio

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)   


## Features of Emailio

- Send Email with attachment
- Uses the Simple Mail Transfer Protocol (SMTP) to send emails
- Supports attachments of different file types
- Customized Subject Line 
- Customized Email Body 
- If no attachment then we will get "Attachment not Found"

## Usage

- Make sure you have Python installed in your system.
- Run Following command in the CMD.
 ```
  pip install Emailio
  ```
## Example

 ```
if __name__ == '__main__':
    pmu = Emailio()
    host = "smtp.gmail.com"
    port = 587
    sender_email = "ravishankerqa@gmail.com"
    password = "XXXXXX"
    receiver_emails = ["ravishankerlal@gmail.com"]
    file_path = r"C://Users//admin//Downloads//filename.pdf"
    subject = "subject line "
    body_text = "body_text"

    pmu.send_email_with_attachment(host, port, sender_email, password, receiver_emails, file_path,subject,body_text)
  ```

## Note 
- I have tried to implement all the functionality, it might have some bugs also. Ignore that or please try to solve that bug.
