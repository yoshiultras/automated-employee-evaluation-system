import logging
from datetime import datetime, timezone
from typing import Tuple

from api.core.dto import AccountLoginMessage, UserLogin
from api.core.exceptions import (
    UserInvalidEmailException,
    UserInvalidPasswordException,
)
from api.core.interactors import Interactor
from api.core.protocols import EmailSender, UnitOfWork, UserRepository
from api.core.services import AuthService

logger = logging.getLogger(__name__)


class UserLoginInteractor(Interactor[UserLogin, Tuple[None, datetime]]):
    def __init__(
        self,
        uow: UnitOfWork,
        user_repository: UserRepository,
        auth_service: AuthService,
        email_sender: EmailSender,
    ):
        self._uow = uow
        self._user_repository = user_repository
        self._auth_service = auth_service
        self._email_sender = email_sender

    async def execute(self, data: UserLogin) -> Tuple[None, datetime]:
        async with self._uow.pipeline():
            user = await self._user_repository.get_by_email(email=data.email)
            if user is None:
                logger.info(f"invalid email: {data.email})")
                raise UserInvalidEmailException()
            if not self._auth_service.verify_pass(
                data.raw_password, user.password
            ):
                logger.info("invalid password")
                raise UserInvalidPasswordException

            session = self._auth_service.create_session(
                user_id=user.id,  # type: ignore
            )
            await self._user_session_repository.add(session)

        datetime_now = datetime.now().astimezone(timezone.utc)
        account_login_message = AccountLoginMessage(
            datetime=datetime_now, email_recipient=user.email
        )
        await self._email_sender.account_login_message(account_login_message)

        return user, session.id  # type: ignore
