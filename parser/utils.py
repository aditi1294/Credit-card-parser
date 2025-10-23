import re
from dateutil import parser as dateparser

def try_parse_date(text: str):
    try:
        return dateparser.parse(text, fuzzy=True).date().isoformat()
    except Exception:
        return None

def normalize_amount(s: str):
    if not s:
        return None
    s = s.replace(',', '').replace(' ', '')
    m = re.search(r'-?\d+(\.\d+)?', s)
    if not m:
        return None
    return float(m.group())
