import re, json, pdfplumber
from PIL import Image
import pytesseract
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from .utils import try_parse_date, normalize_amount
from .issuers import ISSUER_PATTERNS

# Regex patterns
LAST4_RE = re.compile(r'(?:Card|Account|Acct|ending in|ending)\s*(?:[:#]?\s*)?(\d{4})\b', re.I)
DUE_DATE_RE = re.compile(r'(?:Due Date|Payment Due Date|Amount Due By)\s*[:\-\s]*([A-Za-z0-9, /\-]+)', re.I)
BILLING_CYCLE_RE = re.compile(r'Billing Cycle\s*[:\-\s]*([A-Za-z0-9,\- ]+)', re.I)
TOTAL_BALANCE_RE = re.compile(r'(?:New Balance|Total Amount Due|Amount Due|Current Balance)\s*[:\-\s]*([A-Za-z0-9,.\s₹$€£-]+)', re.I)
AMOUNT_RE = re.compile(r'([₹$€£]?\s*-?\d{1,3}(?:[,\d{3}])*(?:\.\d{2})?)')

@dataclass
class Transaction:
    date: Optional[str]
    description: str
    amount: Optional[float]

@dataclass
class ParseResult:
    issuer: Optional[str]
    last4: Optional[str]
    billing_cycle: Optional[str]
    due_date: Optional[str]
    total_balance: Optional[float]
    transactions: List[Transaction]

class StatementParser:
    def __init__(self, issuer_patterns=None):
        self.issuer_patterns = issuer_patterns or ISSUER_PATTERNS

    def _ocr_page(self, page):
        img = page.to_image(resolution=300).original
        return pytesseract.image_to_string(img)

    def _detect_issuer(self, text):
        for issuer, keys in self.issuer_patterns.items():
            for key in keys:
                if key.lower() in text.lower():
                    return issuer
        return "Unknown"

    def _extract_text(self, pdf_path):
        full_text = ""
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if len(text.strip()) < 50:
                    text = self._ocr_page(page)
                pages.append(text)
                full_text += "\n" + text
        return full_text, pages

    def parse(self, pdf_path: str) -> ParseResult:
        text, pages = self._extract_text(pdf_path)
        issuer = self._detect_issuer(text)

        last4 = (m.group(1) if (m := LAST4_RE.search(text)) else None)
        billing_cycle = (m.group(1).strip() if (m := BILLING_CYCLE_RE.search(text)) else None)
        due_date = try_parse_date(m.group(1)) if (m := DUE_DATE_RE.search(text)) else None
        total_balance = normalize_amount(m.group(1)) if (m := TOTAL_BALANCE_RE.search(text)) else None

        # Extract transactions
        transactions = []
        for page_text in pages:
            for line in page_text.splitlines():
                tokens = line.strip().split()
                if len(tokens) < 3:
                    continue
                # Try first token as date, last as amount
                date = try_parse_date(tokens[0])
                amt = normalize_amount(tokens[-1])
                if date and amt:
                    desc = " ".join(tokens[1:-1])
                    if re.search(r'[A-Za-z]', desc):
                        transactions.append(Transaction(date, desc, amt))

        return ParseResult(
            issuer=issuer,
            last4=last4,
            billing_cycle=billing_cycle,
            due_date=due_date,
            total_balance=total_balance,
            transactions=transactions
        )
