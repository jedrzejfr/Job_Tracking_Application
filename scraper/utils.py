from datetime import datetime, timedelta
import unicodedata
import re
import html


def normalize_text(text):
    """
    Normalize text by removing special characters and encoding issues.
    """
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(u"\u2013", "-", text)  # Replace en dash with hyphen for readability
    text = re.sub(u"\u2014", "-", text)  # Replace em dash with hyphen for readability
    text = re.sub(u"\u2010", "-", text)  # Replace hyphen
    text = re.sub(u"\u00e2\u0080\u0093", "-", text)  # Replace problematic sequence
    text = html.unescape(text)
    return text.strip()


def parse_relative_date(date_text):
    """
    Convert relative dates like "26 days ago" into a formatted date (day/month/year).
    """
    if "today" in date_text.lower() or "just now" in date_text.lower():
        return datetime.now().strftime("%d/%m/%Y")
    elif "day" in date_text:
        try:
            days_ago = int(date_text.split()[0])  # Extract the number of days
            actual_date = datetime.now() - timedelta(days=days_ago)
            return actual_date.strftime("%d/%m/%Y")
        except (ValueError, IndexError):
            pass  # Handle invalid date formats
    return "Date not provided"