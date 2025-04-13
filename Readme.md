# 📧 Email Automation Bot

A Python-powered email automation tool that can send **cold emails**, **follow-ups**, and even **read & respond** to specific messages — all without manual effort. It uses **SMTP** and **IMAP** to fully interact with your email account, making it ideal for job outreach, reminders, and smart auto-responders.

![Email Automation Banner](email.png)

---

## 🚀 Features

- 📤 **Send Bulk Emails** using SMTP  
- 📬 **Read & Filter Inbox** using IMAP  
- 🔍 Keyword-based email parsing and response triggers  
- 📎 **Download Attachments** automatically  
- ⏰ Task scheduling using Python's `schedule` module  
- 🔐 Secure credential management via `.env`  

---

## 🧰 Tech Stack

- **Python**
- **smtplib**, **imaplib**, **email**
- **schedule**, **dotenv**
- *(Optional: pandas, openpyxl for reading `.xlsx`)*

---

## 📂 Project Structure

```
email-automater/
├── main.py               # Cold email sender
├── follow_up.py          # Follow-up script
├── email_reader.py       # Inbox parsing and auto-response
├── templates/            # Email content templates
├── hr_updated.xlsx       # Recipient list
├── .env                  # Secure email credentials
└── requirements.txt
```

---

## 🧪 How to Use

1. ✅ Clone the repo  
2. ✅ Install requirements  
   ```
   pip install -r requirements.txt
   ```
3. ✅ Setup your `.env` file like:
   ```
   EMAIL=your.email@example.com
   EMAIL_PASSWORD=yourpassword
   ```
4. ✅ Run the cold email sender:
   ```
   python main.py
   ```
5. ✅ After 7 days, trigger follow-ups:
   ```
   python follow_up.py
   ```

---

## 🔐 Note

This repo code is not uploaded completely 
📩 Contact me for access — complete code available on request due to NDA/confidentiality.

---

## 🌟 Want More?

Want to level up this bot with:
- 📊 Analytics & open tracking  
- 🤖 GPT-powered response generator  
- 🔗 LinkedIn scraping & integration  

> Just reach out! I’d love to collaborate.
