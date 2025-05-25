
import pdfplumber
import re
import pandas as pd
from io import BytesIO

def extract_transactions_from_pdf(pdf_file):
    with pdfplumber.open(BytesIO(pdf_file)) as pdf:
        text = "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )

    # Extract individual transactions based on UPI pattern
    lines = text.splitlines()
    transactions = []
    for i in range(len(lines)):
        line = lines[i]
        if re.match(r"^\d{2}\s\w{3}", line):  # date pattern like "12 Jul"
            try:
                date = line.strip()
                description = lines[i+1].strip()
                amount_line = lines[i+2].strip()
                amount_match = re.search(r"([+-]\s*Rs\.?\s?\d+[,.]?\d*)", amount_line)
                if amount_match:
                    amount = amount_match.group(1).replace(" ", "").replace("Rs", "").replace("+", "").replace(",", "")
                    amount = float(amount) if "-" not in amount_line else -float(amount)
                    transactions.append({
                        "Date": date,
                        "Description": description,
                        "Amount": amount
                    })
            except IndexError:
                continue

    df = pd.DataFrame(transactions)
    return df
