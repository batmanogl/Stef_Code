import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Before you run the script, you can make a connectivity test: ping smtp.gmail.com

# Gmail SMTP server configuration
smtp_server = "smtp.gmail.com"
port = 587
login = "sbatmanoglou@gmail.com"  # Your Gmail address
password = "hhmh mwhx dysl ****"  # Use a Gmail App Password

sender_email = "sbatmanoglou@gmail.com"
receiver_email = "sbatmanoglou@gmail.com"

# Email content
subject = "Your Driving License Expires Soon"
body = "Please contact us as soon as possible, as your driving license is about to expire."

# Create email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the text part
message.attach(MIMEText(body, "plain"))

try:
    # Connect to Gmail SMTP server
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Secure connection
        server.login(login, password)  # Log in
        server.sendmail(sender_email, receiver_email, message.as_string())  # Send email

    print("Email sent successfully.")

except smtplib.SMTPAuthenticationError:
    print("Authentication failed. Please check your email and App Password settings.")
except smtplib.SMTPException as e:
    print(f"SMTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")


