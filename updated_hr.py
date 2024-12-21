import pandas as pd
import re
import logging
import os

# === Configuration ===
input_file_path = './data/Hr_emails.xlsx'  # Input Excel file path
output_file_path = './data/hr_updated.xlsx'  # Output Excel file path
log_dir = './logs/'
invalid_email_log = os.path.join(log_dir, 'invalid_emails.log')
update_log = os.path.join(log_dir, 'email_update.log')

# Ensure log directory exists
os.makedirs(log_dir, exist_ok=True)

# === Configure Logging ===
logging.basicConfig(
    filename=update_log, 
    filemode='a', 
    format='%(asctime)s - %(message)s', 
    level=logging.INFO
)

# === Read Excel File ===
try:
    df = pd.read_excel(input_file_path)
    logging.info(f"Successfully read input file: {input_file_path}")
except Exception as e:
    logging.error(f"Error reading input file {input_file_path}: {e}")
    raise

# === Clean the Email Column ===
def clean_email(email):
    """Clean the email by removing extra spaces, commas, and special characters."""
    if pd.isnull(email):
        return ''
    cleaned_email = re.sub(r'[^a-zA-Z0-9@._-]', '', email.strip())
    if '@' in cleaned_email:
        return cleaned_email 
    else:
        with open(invalid_email_log, 'a') as f:
            f.write(f"Invalid email: {email}\n")
        return ''

df['Email'] = df['Email'].apply(clean_email)

# === Add New Columns (Name and Company) ===
def extract_name_from_email(email):
    """Extract name from the email (before the @) and capitalize it."""
    if pd.notnull(email) and '@' in email:
        return email.split('@')[0].capitalize()
    return ''

def extract_company_from_email(email):
    """Extract company from the email (between @ and .) and capitalize it."""
    if pd.notnull(email) and '@' in email:
        domain = email.split('@')[1] if '.' in email.split('@')[1] else ''
        company = domain.split('.')[0] if domain else ''
        return company.capitalize()
    return ''

df['Name'] = df['Email'].apply(extract_name_from_email)
df['Company'] = df['Email'].apply(extract_company_from_email)

# === Ensure the 'Mention_Specific_Qualities' column exists ===
if 'Mention_Specific_Qualities' not in df.columns:
    df['Mention_Specific_Qualities'] = ''  # Initialize as an empty string

# === Function to Assign Default Mention Qualities ===
def assign_mention_qualities(company):
    """Return specific qualities for the given company."""
    default_mention_qualities = {
        'oracle': 'its industry leadership in enterprise software and database technology, enabling seamless business transformation worldwide',
        'bobtechsolutions': 'its dedication to delivering cutting-edge IT consulting and staffing services that bridge the talent gap with precision',
        'igatepatni': 'its legacy of excellence in IT services and its innovative approach to delivering value-driven customer solutions',
        'creativesolution': 'its forward-thinking, customer-centric approach to offering unique and customized business solutions',
        'emacstech': 'its specialization in modern technology solutions and commitment to fostering client-centric software development',
        'google': 'its groundbreaking work in AI, search technology, and its mission to organize the world’s information for universal access',
        'microsoft': 'its transformative impact on cloud computing, software development, and its vision for "Empowering every person and every organization on the planet to achieve more"',
        'infosys': 'its role as a global leader in next-generation digital services and its mission to navigate clients through their digital transformation journeys',
        'tcs': 'its status as a global powerhouse in IT services and its commitment to driving digital transformation with agility and innovation',
        'wipro': 'its human-centric approach to delivering innovative digital transformation and consulting solutions for businesses worldwide',
        'accenture': 'its forward-looking approach to strategy, consulting, and technology services that drive global business excellence',
        'capgemini': 'its excellence in engineering and R&D services, known for enabling global businesses to achieve digital transformation',
        'cognizant': 'its commitment to helping clients modernize technology, reimagine processes, and transform customer experiences',
        'hcltech': 'its strong focus on innovation, next-generation IT services, and customer-first digital solutions',
        'mindtree': 'its excellence in crafting seamless digital experiences for customers through technology and human-centered design',
        'deloitte': 'its unmatched expertise in strategy, analytics, and audit services, helping organizations make informed, future-ready decisions',
        'ey': 'its leadership in consulting, audit, and financial advisory services, with a focus on driving long-term business value',
        'kpmg': 'its mission to empower businesses with strategic financial insights and risk management expertise',
        'pwc': 'its expertise in tax, audit, and consulting services, supporting organizations with sustainable strategies for long-term growth',
        'techmahindra': 'its commitment to providing world-class IT services and engineering solutions with a focus on the telecom sector',
        'samsung': 'its relentless drive for innovation in electronics, semiconductors, and technology that defines the future of smart devices',
        'intel': 'its leadership in semiconductor innovation, AI acceleration, and commitment to powering the world’s data-driven future',
        'ibm': 'its legacy of pioneering innovation in AI, hybrid cloud, and business transformation, leading enterprises into the era of smart technology',
        'adobe': 'its ability to revolutionize digital experiences and creative software tools that empower individuals and enterprises alike',
        'amazon': 'its obsession with customer satisfaction, operational excellence, and its role in shaping the future of e-commerce and cloud computing',
        'flipkart': 'its transformative role in India’s e-commerce landscape, driving affordability, customer satisfaction, and innovation',
        'paytm': 'its leadership in digital payments, fintech innovation, and its role in driving India’s cashless economy',
        'phonepe': 'its trusted position as a leading digital payments platform, simplifying transactions and enhancing customer convenience',
        'reliance': 'its influence as a leader in diversified industries, driving India’s economic development and innovation in telecom, retail, and energy',
        'byjus': 'its impact on transforming education through cutting-edge online learning and personalized learning experiences',
        'zoho': 'its reputation for creating world-class, cost-effective business software solutions to empower startups, SMBs, and enterprises',
        'freshworks': 'its innovative cloud-based software solutions that make customer engagement and support simpler, faster, and more effective',
        'upgrad': 'its role in redefining online education, upskilling professionals, and fostering lifelong learning opportunities',
        'zomato': 'its focus on connecting customers with their favorite foods through technology-driven food delivery services',
        'swiggy': 'its role in redefining India’s food delivery ecosystem with convenience, customer-first services, and tech-driven logistics',
        'ola': 'its commitment to providing safe, reliable, and sustainable ridesharing and urban mobility solutions',
        'uber': 'its focus on revolutionizing urban mobility, enabling seamless ride-hailing services powered by smart technology',
        'airbnb': 'its role in transforming global travel and hospitality with unique, community-driven lodging experiences',
        'linkedin': 'its mission to connect professionals around the world and enable them to be more productive and successful',
        'netflix': 'its pioneering role in the entertainment industry, redefining content consumption through on-demand streaming services',
        'spotify': 'its innovation in music streaming, delivering a personalized, on-demand listening experience to millions worldwide',
        'salesforce': 'its revolutionary approach to customer relationship management (CRM) software that empowers businesses to connect with customers like never before',
        'tesla': 'its groundbreaking contributions to electric vehicles, renewable energy, and the future of sustainable transportation',
        'spaceX': 'its audacious mission to make life multi-planetary, pushing the boundaries of space exploration and aerospace innovation',
        'bitwise': 'its emphasis on data-driven software development, helping organizations turn insights into actionable decisions',
        'morganstanley': 'its leadership in global financial services, offering a trusted platform for wealth management and investment banking',
        'goldmansachs': 'its impact on shaping global financial markets, with leadership in investment banking, securities, and asset management',
        'jpmorganchase': 'its global influence as a financial powerhouse, leading in banking, asset management, and financial services',
        'bankofamerica': 'its role in advancing global financial inclusion, offering a wide range of financial services for individuals and businesses',
        'axisbank': 'its customer-first approach to delivering secure, innovative, and personalized banking solutions',
        'hdfcbank': 'its excellence in providing innovative financial products and services that enhance the banking experience',
        'icicibank': 'its commitment to modernizing banking and providing customer-centric, tech-enabled financial services',
    }

    company_key = company.lower() if isinstance(company, str) else ''
    return default_mention_qualities.get(company_key, 'its commitment to excellence and innovation')

df['Mention_Specific_Qualities'] = df.apply(
    lambda row: row['Mention_Specific_Qualities'] if pd.notnull(row['Mention_Specific_Qualities']) and row['Mention_Specific_Qualities'].strip() 
    else assign_mention_qualities(row['Company']), axis=1
)

# === Add New Columns for Sent Date, Opened, and Replied ===
if 'Sent Date' not in df.columns:
    df['Sent Date'] = ''  # Empty for now, to be updated when emails are sent
if 'Opened' not in df.columns:
    df['Opened'] = False  # Default is False, to be updated when an email is opened
if 'Replied' not in df.columns:
    df['Replied'] = False  # Default is False, to be updated when an email is replied to
if 'Follow-Up Sent' not in df.columns:
    df['Follow-Up Sent'] = False  # Default is False, to be updated when an email is Follow-Up Sent to

# === Save the Updated File ===
try:
    df.to_excel(output_file_path, index=False)
    logging.info(f"Successfully saved updated file: {output_file_path}")
except Exception as e:
    logging.error(f"Error saving updated file {output_file_path}: {e}")

# === Log the Results ===
total_records = len(df)
invalid_emails = sum(df['Email'] == '')
updated_records = total_records - invalid_emails

logging.info(f"Total records processed: {total_records}")
logging.info(f"Successfully updated records: {updated_records}")
logging.info(f"Total invalid emails: {invalid_emails}")

print(f"Updated file saved as {output_file_path}")
print(f"Log file created at {update_log}")
