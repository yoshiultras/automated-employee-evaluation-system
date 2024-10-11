from typing import Protocol

from api.core.dto import AccountLoginMessage


class EmailSender(Protocol):
    async def account_login_message(self, data: AccountLoginMessage) -> None:
        raise NotImplementedError
