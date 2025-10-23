
# 💳 Credit Card Statement Parser

### 🧠 Overview  
This project extracts key financial details from **Indian credit card statements (PDFs)** using **Python** and **Streamlit**.  
It supports multiple banks and helps you quickly view billing details, due dates, and transaction summaries in a clean interface.

---

## ⚙️ Features
- 🏦 Supports 5 major Indian issuers: **HDFC**, **ICICI**, **SBI**, **Axis**, and **American Express**
- 🔍 Extracts 5 key data points:
  - Issuer Name  
  - Card Last 4 Digits  
  - Billing Cycle  
  - Payment Due Date  
  - Total Balance + Transaction History
- 💻 Interactive Streamlit UI  
- 💾 Download parsed data as **JSON**

---

## 🚀 How to Run

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
````

### 2️⃣ Add PDF Files

Place your sample credit card statements in the `sample_statements/` folder.

### 3️⃣ Launch the App

```bash
streamlit run app.py
```

### 4️⃣ Use the Interface

* Upload a statement PDF
* View extracted issuer, billing cycle, and transactions
* Download results as a JSON file

---

## 🏦 Supported Issuers

Defined in `parser/issuers.py`:

```python
ISSUER_PATTERNS = {
    "HDFC Bank": ["HDFC", "HDFC BANK"],
    "ICICI Bank": ["ICICI", "ICICI BANK"],
    "SBI Card": ["SBI", "STATE BANK OF INDIA"],
    "Axis Bank": ["AXIS", "AXIS BANK"],
    "American Express": ["AMEX", "AMERICAN EXPRESS"]
}
```

---

## 📄 Example Output

```json
{
  "issuer": "HDFC Bank",
  "last4": "5678",
  "billing_cycle": "01 Jan - 31 Jan 2025",
  "due_date": "20 Feb 2025",
  "total_balance": 25430.75
}
```

---

### 🖤 Built with Python & Streamlit

Simple • Fast • Reliable

```
