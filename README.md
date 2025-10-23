Credit Card Statement Parser

Overview:
This project extracts key financial details from Indian credit card statements (PDFs) using Python and Streamlit.
It supports multiple banks and helps quickly view your billing details and transactions in a structured format.

Features

Supports 5 major Indian issuers: HDFC, ICICI, SBI, Axis, American Express

Extracts 5 key data points:

Issuer Name

Card Last 4 Digits

Billing Cycle

Payment Due Date

Total Balance + Transactions

Clean Streamlit UI with JSON download option

How to Run

Install dependencies

pip install -r requirements.txt

Place PDF files in the sample_statements/ folder

Run the Streamlit app

streamlit run app.py

Upload a statement and view parsed details instantly

Download results as a JSON file

Supported Issuers

Defined in parser/issuers.py:

ISSUER_PATTERNS = {
    "HDFC Bank": ["HDFC", "HDFC BANK"],
    "ICICI Bank": ["ICICI", "ICICI BANK"],
    "SBI Card": ["SBI", "STATE BANK OF INDIA"],
    "Axis Bank": ["AXIS", "AXIS BANK"],
    "American Express": ["AMEX", "AMERICAN EXPRESS"]
}

🖤Built with Python & Streamlit

Simple. Fast. Reliable.