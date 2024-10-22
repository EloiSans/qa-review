import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Define the email parameters
sender_email = "sender@example.com"
receiver_email = "receiver@example.com"
subject = "Test Email with HTML from Python"
body_text = "This is a test email sent using Mailpit and Python."
body_html = """
<html>
<head></head>
<body>
    <h1>Test Email</h1>
    <p>This is a <b>test email</b> sent using <a href="https://mailpit.dev">Mailpit</a> and Python.</p>
</body>
</html>
"""

# Create the email message
msg = MIMEMultipart("alternative")
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the plain text part
part1 = MIMEText(body_text, 'plain')
msg.attach(part1)

# Attach the HTML part
part2 = MIMEText(body_html, 'html')
msg.attach(part2)

# Connect to the Mailpit SMTP server
smtp_server = "localhost"
smtp_port = 1025

try:
    # Create an SMTP session
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")

response = requests.get("http://localhost:8025/api/v1/message/latest", headers={"accept": "application/json"})
print(response.json())
_subject = response.json()['Subject']
assert subject == _subject
