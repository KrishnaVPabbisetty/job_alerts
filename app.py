from flask import Flask, request, jsonify, render_template
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# List to store emails (in a production app, store this in a database)
emails = []

# Email details
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))

# Function to send email notifications
def send_email(subject, message, receiver_email):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        # Connect to the Gmail SMTP server
        with SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, password)  # Log in to the email account
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
@app.route('/')
def home():
    return render_template('index.html') 

# Route to handle email submission
@app.route('/submit-email', methods=['POST'])
def submit_email():
    data = request.get_json()
    email = data.get('email')
    
    if email:
        emails.append(email)  # Save the email to the list (or save to DB)
        
        # Send the email to the user (or use a job fetching function to send Amazon jobs)
        send_email("Amazon Job Notifications", "You will receive job notifications soon.", email)
        
        # Send the email to all users (you can integrate the job notification functionality here)
        # For example, send the latest Amazon job notifications to all users in the emails list
        for user_email in emails:
            send_email("New Job Listings on Amazon", "Here are the latest Amazon job listings.", user_email)

        return jsonify({"message": "Email submitted successfully!"}), 200
    return jsonify({"message": "Email is required."}), 400

if __name__ == "__main__":
    app.run(debug=True)