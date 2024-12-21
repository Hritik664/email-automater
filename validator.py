import re

def is_valid_email(email):
    """
    Validates an email address using a regular expression pattern.
    Returns True if the email is valid, otherwise False.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def filter_valid_emails(email_list):
    """
    Filters a list of email addresses and returns only the valid ones.
    """
    valid_emails = [email for email in email_list if is_valid_email(email)]
    return valid_emails


if __name__ == "__main__":
    # Example email list for testing
    test_emails = [
        'hritik@gmail.com', 
        'test-email@domain.com', 
        'invalid-email@domain', 
        'user@@domain.com', 
        'user@domain.co.in', 
        'valid.email+tag@gmail.com', 
        'wrong_email@.com'
    ]
    
    print("All Emails:", test_emails)
    valid_emails = filter_valid_emails(test_emails)
    print("Valid Emails:", valid_emails)
