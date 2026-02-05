import re

def extract_info(text):
    upi = re.findall(r'\b[\w.-]+@[\w.-]+\b', text)
    urls = re.findall(r'https?://\S+', text)
    accounts = re.findall(r'\b\d{9,18}\b', text)
    ifsc = re.findall(r'[A-Z]{4}0[A-Z0-9]{6}', text)

    return {
        "upi_ids": list(set(upi)),
        "bank_accounts": list(set(accounts)),
        "ifsc_codes": list(set(ifsc)),
        "phishing_links": list(set(urls)),
    }
