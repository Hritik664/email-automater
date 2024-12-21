# import pandas as pd
# import smtplib
# import socket
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# from dotenv import load_dotenv
# import os
# import time

# # === Load Environment Variables ===
# load_dotenv()

# # === Configuration ===
# excel_path = 'hr_updated.xlsx'  # Path to the updated Excel file
# sender_email = os.getenv('EMAIL')  # Your email address from .env
# email_password = os.getenv('EMAIL_PASSWORD')  # Your app-specific password
# resume_path = 'Hritik_Singh_Resume_MERN.pdf'  # Path to your resume file
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587

# # === Read Excel File ===
# df = pd.read_excel(excel_path)

# # === Email Template (Updated for Professional Cold Email) ===
# email_subject = "Exploring Career Opportunities at {company_name}"
# email_body = """
# Hi {name},

# I hope you are doing well. My name is Hritik Singh, and I am a passionate Software Engineer with a solid foundation in Python, Data Structures, and Full-Stack Development. I am reaching out to explore potential career opportunities at {company_name}.

# I am particularly drawn to {company_name} because of {mention_specific_qualities}. I believe my technical skills, problem-solving abilities, and passion for continuous learning could make me a valuable contributor to your team.

# I would be delighted to connect and discuss how I can support {company_name}'s ongoing projects and initiatives. Please find my resume attached for your reference.

# Thank you for your time and consideration. I look forward to hearing from you.

# Best regards,  
# Hritik Singh  
# Email: singhhritik560@gmail.com  
# Phone: +91 9335328103  

# *Note: This email was thoughtfully crafted and sent with the help of automation to ensure timely delivery and personalized messaging.

# Creater of this Email Automation - Hritik Singh*
# """

# # === Email Sending Configuration ===
# server = smtplib.SMTP(smtp_server, smtp_port)
# server.starttls()
# server.login(sender_email, email_password)

# # === Batch Configuration ===
# total_rows = len(df)
# batch_size = 20  # Send 20 emails at a time
# start_index = int(os.getenv('START_INDEX', 0))  # Get the start index from environment variables
# end_index = min(start_index + batch_size, total_rows)  # End index for current batch

# # === Email Validation Function (to prevent sending to invalid emails) ===
# def is_valid_email(email):
#     """Check if the email domain is valid by attempting to resolve its MX records."""
#     try:
#         domain = email.split('@')[1]
#         socket.gethostbyname(domain)
#         return True
#     except Exception as e:
#         print(f"Invalid email domain for {email}: {e}")
#         return False

# # === Send Emails in Batches ===
# for index, row in df.iloc[start_index:end_index].iterrows():
#     email = row.get('Email')
#     name = row.get('Name')
#     company_name = row.get('Company')
#     mention_specific_qualities = row.get('Mention_Specific_Qualities', 'its commitment to excellence')

#     if pd.isnull(email) or pd.isnull(name) or pd.isnull(company_name):
#         print(f"Skipping row {index} due to missing data.")
#         continue

#     # Check if the email is valid before sending
#     if not is_valid_email(email):
#         print(f"Skipping email {email} due to invalid domain.")
#         continue

#     try:
#         subject = email_subject.format(company_name=company_name)
#         body = email_body.format(
#             name=name, 
#             company_name=company_name, 
#             mention_specific_qualities=mention_specific_qualities
#         )

#         message = MIMEMultipart()
#         message['From'] = sender_email
#         message['To'] = email
#         message['Subject'] = subject
#         message.attach(MIMEText(body, 'plain'))

#         # Attach the resume
#         with open(resume_path, 'rb') as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(resume_path)}')
#             message.attach(part)

#         server.sendmail(sender_email, email, message.as_string())
#         print(f"Email successfully sent to {name} at {email}.")
        
#         time.sleep(2)  # Wait to avoid Gmail spam filters
#     except Exception as e:
#         print(f"Failed to send email to {email}: {e}")

# server.quit()

# # === Update the Start Index ===
# next_start_index = end_index if end_index < total_rows else 0  # Reset if all emails are sent
# with open('.env', 'w') as env_file:
#     env_file.write(f"START_INDEX={next_start_index}\n")
#     env_file.write(f"EMAIL={sender_email}\n")
#     env_file.write(f"EMAIL_PASSWORD={email_password}\n")

# print(f"Batch completed. Next start index is {next_start_index}")



# ======================================================================================================

# import os
# import smtplib
# import pandas as pd
# import random
# import time
# import logging
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# from dotenv import load_dotenv
# from validator import is_valid_email

# # Load environment variables from .env file
# load_dotenv()

# # Global Variables
# SENDER_EMAIL = os.getenv('EMAIL')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
# START_INDEX = int(os.getenv('START_INDEX', 0))  # Default to 0 if not set
# EMAIL_BATCH_SIZE = 50  # Number of emails to send in each batch
# DELAY_BETWEEN_EMAILS = random.randint(30, 60)  # Random delay to avoid spam detection

# # Log file for email errors
# logging.basicConfig(filename='logs/email_log.txt', level=logging.ERROR)

# # Load the HR email data
# df = pd.read_excel('data/hr_updated.xlsx')


# def send_email(to_email, name, company, attachment='Hritik_Singh_Resume_MERN.pdf'):
#     """Sends a personalized email to the recipient."""
#     try:
#         # Create the email message
#         subject = f"Excited to Apply at {company} - MERN Developer Role"
#         message = MIMEMultipart()
#         message['From'] = SENDER_EMAIL
#         message['To'] = to_email
#         message['Subject'] = subject

#         # Load the email templates and choose one at random
#         with open('email_templates.txt', 'r', encoding='utf-8') as file:
#             templates = file.read().split('---')
#         email_body = random.choice(templates)

#         # Replace placeholders with dynamic content
#         email_body = email_body.replace('{name}', name).replace('{company}', company)

#         # Attach the email body
#         message.attach(MIMEText(email_body, 'html'))

#         # Attach the resume file
#         with open(attachment, 'rb') as attachment_file:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment_file.read())
#         encoders.encode_base64(part)
#         part.add_header('Content-Disposition', f'attachment; filename={attachment}')
#         message.attach(part)

#         # Connect to the Gmail server
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, EMAIL_PASSWORD)
#         server.sendmail(SENDER_EMAIL, to_email, message.as_string())
#         server.quit()

#         print(f"✅ Email sent to {name} at {to_email}.")
#         return True

#     except Exception as e:
#         logging.error(f"❌ Failed to send email to {to_email}: {e}")
#         return False


# def update_tracking(email, status, column_name):
#     """Update the tracking file (hr_updated.xlsx) to log sent, opened, and replied status."""
#     try:
#         df.loc[df['Email'] == email, column_name] = status
#         df.to_excel('data/hr_updated.xlsx', index=False)
#     except Exception as e:
#         logging.error(f"❌ Failed to update tracking for {email}: {e}")


# def send_batch_emails(start_index=0, batch_size=EMAIL_BATCH_SIZE):
#     """Sends emails in batches, with a delay between each email to avoid spam detection."""
#     total_emails = len(df)
#     for index in range(start_index, start_index + batch_size):
#         if index >= total_emails:
#             print("✅ All emails have been sent.")
#             break

#         row = df.iloc[index]
#         email = row['Email']
#         name = row['Name'] if 'Name' in row else 'HR'
#         company = row['Company'] if 'Company' in row else 'the company'

#         # Check if email is valid
#         if not is_valid_email(email):
#             update_tracking(email, 'Invalid Email', 'Status')
#             print(f"❌ Skipping invalid email: {email}")
#             continue

#         # Send the email
#         success = send_email(email, name, company)
#         if success:
#             update_tracking(email, 'Sent', 'Status')
#             update_tracking(email, pd.Timestamp.now(), 'Sent Date')

#         # Random delay to avoid spam detection
#         sleep_time = random.randint(30, 60)
#         print(f"⏲️ Sleeping for {sleep_time} seconds...")
#         time.sleep(sleep_time)


# if __name__ == "__main__":
#     print("🚀 Starting batch email sending...")
#     send_batch_emails(start_index=START_INDEX)
#     print("✅ Batch email process completed.")



# ================================================================================================================================
import os
import smtplib
import pandas as pd
import random
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from validator import is_valid_email

# Load environment variables from .env file
load_dotenv()

# Global Variables
SENDER_EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
START_INDEX = int(os.getenv('START_INDEX', 0))
EMAIL_BATCH_SIZE = 50
DELAY_BETWEEN_EMAILS = random.randint(30, 120)

# Log configuration
log_filename = f'logs/email_log_{pd.Timestamp.now().strftime("%Y-%m-%d")}.txt'
logging.basicConfig(filename=log_filename, level=logging.INFO)

# Load HR email data
df = pd.read_excel('data/hr_updated.xlsx')

def send_email(to_email, name, company, mention_specific_qualities, attachment='Hritik_Singh_Resume_MERN.pdf'):
    try:
        subject = f"Excited to Apply at {company} - MERN Developer Role"
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = to_email
        message['Subject'] = subject
        message['Reply-To'] = SENDER_EMAIL

        with open('./templates/email_templates.txt', 'r', encoding='utf-8') as file:
            templates = file.read().split('---')
        email_body = random.choice(templates).replace('{name}', name).replace('{company}', company).replace('{mention_specific_qualities}', mention_specific_qualities)
        tracking_pixel = f'<img src="https://your-server.com/track_open?email={to_email}" width="1" height="1" style="display:none;">'
        email_body += tracking_pixel
        message.attach(MIMEText(email_body, 'html'))

        with open(attachment, 'rb') as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment}')
        message.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, message.as_string())
        server.quit()

        logging.info(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        logging.error(f"❌ Failed to send email to {to_email}: {e}", exc_info=True)
        return False

def update_tracking(email, status, column_name):
    try:
        df.loc[df['Email'] == email, column_name] = status
        df.to_excel('data/hr_updated.xlsx', index=False)
    except Exception as e:
        logging.error(f"❌ Failed to update tracking for {email}: {e}", exc_info=True)

def send_batch_emails(start_index=0, batch_size=EMAIL_BATCH_SIZE):
    try:
        for index in range(start_index, start_index + batch_size):
            if index >= len(df):
                print("✅ All emails have been sent.")
                break

            row = df.iloc[index]
            email = row['Email']
            if not is_valid_email(email):
                update_tracking(email, 'Invalid Email', 'Status')
                continue

            success = send_email(email, row.get('Name', 'HR'), row.get('Company', 'the company'), row.get('Mention_Specific_Qualities', 'its commitment to excellence and innovation'))
            if success:
                update_tracking(email, 'Sent', 'Status')
                update_tracking(email, pd.Timestamp.now(), 'Sent Date')

            sleep_time = random.randint(30, 120)
            print(f"⏲️ Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logging.warning("🚪 User interrupted the process. Exiting gracefully...")

if __name__ == "__main__":
    print("🚀 Starting batch email sending...")
    send_batch_emails(start_index=START_INDEX)
    print("✅ Batch email process completed.")
