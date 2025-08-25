"""
Author: Akshay NS
Contains: EmailFetcher using IMAP

"""

import imaplib, email
from typing import List, Optional
from app.domain.services.email_fetch_service import EmailFetchService
from app.domain.models.user_credentials import UserCredentials
from app.domain.models.email import Email


class EmailFetcherIMAP(EmailFetchService):
    def fetch(
        self,
        user_credentials: UserCredentials,
        limit: int = 10,# e.g. 50
        since: Optional[str] = None,  # e.g. "01-Jan-2024"
    ) -> List[Email]:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user_credentials.email, user_credentials.password)
        mail.select("inbox")

        # Build search query
        search_criteria = "ALL"
        if since:
            search_criteria = f'(SINCE "{since}")'

        status, messages = mail.search(None, search_criteria)
        email_ids = messages[0].split()

        # If limiting, grab only the last N
        if limit:
            email_ids = email_ids[-limit:]

        emails = []
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            subject = msg["subject"]
            sender = msg["from"]
            sent_at = msg["date"]

            if msg.is_multipart():
                body = ""
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode(errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            emails.append(
                Email(
                    id=None,
                    sender=sender,
                    subject=subject,
                    body=body,
                    sent_at=sent_at,
                    category="inbox",
                )
            )

        mail.logout()
        return emails
