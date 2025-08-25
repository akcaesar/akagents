"""
Author: Akshay NS
Contains: Using BeautifulSoup to clean email content.

"""


from app.domain.services.email_content_cleaner import EmailContentCleaner
from bs4 import BeautifulSoup
import re


class EmailContentCleanBS4(EmailContentCleaner):
   def clean(self, raw_body: str) -> str:
    """
    Process email body (plain text or HTML) and return clean main content.
    - Removes scripts, styles, metadata, signatures
    - Strips extra whitespace
    """
    if not raw_body:
        return ""

    # If it's HTML, parse with BeautifulSoup
    if raw_body.lstrip().lower().startswith("<!doctype") or "<html" in raw_body.lower():
        soup = BeautifulSoup(raw_body, "html.parser")

        # Kill unwanted tags
        for tag in soup(["script", "style", "meta", "head", "title", "link"]):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator=" ")

    else:
        # Already plain text
        text = raw_body

    # Collapse multiple spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()

    # Optionally: remove common email footer markers ("Sent from my iPhone", etc.)
    # Here just an example:
    footer_markers = ["sent from my iphone", "--", "unsubscribe"]
    for marker in footer_markers:
        idx = text.lower().find(marker)
        if idx != -1:
            text = text[:idx].strip()
            break

    return text