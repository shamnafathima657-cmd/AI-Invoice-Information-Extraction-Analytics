import re
# -----------------------------
# Company Name
# -----------------------------
def extract_company(text):

    match = re.search(r"ABC\s+Super\s+Market", text, re.I)

    if match:
        return match.group()

    return ""

# -----------------------------
# Invoice Number
# -----------------------------
def extract_invoice_number(text):

    patterns = [

        r"Invoice\s*#\s*([A-Za-z0-9\-]+)",

        r"Invoice\s*No[:\s]*([A-Za-z0-9\-]+)",

        r"Invoice\s*Number[:\s]*([A-Za-z0-9\-]+)",

        r"Receipt\s*No[:\s]*([A-Za-z0-9\-]+)"

    ]

    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return m.group(1)

    return ""

# -----------------------------
# Date
# -----------------------------
def extract_date(text):

    patterns = [

    r"\d{2}/\d{2}/\d{4}",

    r"\d{2}-\d{2}-\d{4}",

    r"\d{4}-\d{2}-\d{2}",

    r"\d{2}\s+[A-Za-z]{3}\s+\d{4}"

    ]



    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group()

    return ""


# -----------------------------
# Tax
# -----------------------------
def extract_tax(text):

    match = re.search(r"GST\s*\(\d+%\)\s*([\d,]+\.\d{2})", text, re.I)

    if match:
        return match.group(1).replace(",", "")

    return ""

# -----------------------------
# Payment Method
# -----------------------------
def extract_payment(text):

    methods = [

        "Cash",

        "Card",

        "Credit Card",

        "Debit Card",

        "Visa",

        "MasterCard",

        "UPI",

        "Online",

        "Bank Transfer"
    ]

    for method in methods:

        if method.lower() in text.lower():
            return method

    return ""


# -----------------------------
# Total Amount
# -----------------------------
def extract_total(text):

    patterns = [

        r"Total Amount\s*[:₹RM${\s]*([\d,]+\.\d{2})",

        r"Grand Total\s*[:₹RM${\s]*([\d,]+\.\d{2})",

        r"Amount Due\s*[:₹RM${\s]*([\d,]+\.\d{2})"

    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).replace(",", "")

    return ""

# -----------------------------
# Clean OCR Amount
# -----------------------------
def clean_amount(amount):

    if not amount:
        return ""

    amount = amount.replace(",", "")

    # Fix OCR errors like 71203.60 -> 1203.60
    if amount.startswith("71") and len(amount) >= 7:
        amount = amount[1:]

    return amount

# =========================================================
# MAIN FUNCTION
# =========================================================
def extract_invoice_data(text):

    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    result = {

    "Company Name": extract_company(text),

    "Invoice Number": extract_invoice_number(text),

    "Invoice Date": extract_date(text),

    "Tax": clean_amount(extract_tax(text)),

    "Payment Method": extract_payment(text),

    "Total Amount": clean_amount(extract_total(text))
    }

    return result


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    sample = """
    SANYU STATIONERY SHOP
    No.31G Jalan Setia Indah
    Invoice No: CS-SA-0119537
    Date: 24/10/2017
    Cash
    Total RM 3.00
    """

    print(extract_invoice_data(sample))