from dataclasses import dataclass
from datetime import datetime


@dataclass
class AccountLoginMessage:
    datetime: datetime
    email_recipient: str
