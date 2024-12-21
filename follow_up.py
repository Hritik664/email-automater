import pandas as pd
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# === Load Environment Variables ===
load_dotenv()

# === Configuration ===
excel_path = 'data/hr_updated.xlsx'
sender_email = os.getenv('EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# === Logger Setup ===
logging.basicConfig(filename='logs/email_log.txt', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# === Read Excel File ===
df = pd.read_excel(excel_path)

today = datetime.now()

# === Start SMTP Server ===
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, email_password)

for index, row in df.iterrows():
    email = row.get('Email')
    name = row.get('Name')
    company_name = row.get('Company')
    sent_date = pd.to_datetime(row.get('Sent Date'))
    status = row.get('Replied')
    
    if pd.isnull(sent_date) or status != 'Sent':
        continue  # Skip rows where no email was sent
    
    days_since_sent = (today - sent_date).days
    
    if days_since_sent >= 7 and row.get('Follow-Up Sent') != 'YES':
        try:
            subject = f"Just checking in on my previous email about {company_name}"
            body = f"Hi {name},\n\nI hope you're doing well. I wanted to follow up on my previous email regarding potential opportunities at {company_name}. Please let me know if you'd like to discuss further.\n\nBest Regards,\nHritik Singh"
            
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            
            server.sendmail(sender_email, email, message.as_string())
            print(f"Follow-up email sent to {name} at {email}.")
            df.at[index, 'Follow-Up Sent'] = 'YES'
        except Exception as e:
            print(f"Failed to send follow-up email to {email}: {e}")
            logging.error(f"Failed to send follow-up email to {email}: {e}")

server.quit()

# === Save the Updated File ===
df.to_excel(excel_path, index=False)

print("Follow-up batch completed.")
