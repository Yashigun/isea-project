from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.security.refresh_tokens import hash_refresh_token, verify_refresh_token_hash
from app.repositories.store.customer_repository import CustomerRepository
from app.repositories.security.customer_session_repository import CustomerSessionRepository
from app.repositories.security.login_attempt_repository import LoginAttemptRepository
from app.models.store.customer import Customer, AccountStatus, AuthProvider
from app.models.security.customer_session import CustomerSession
from app.models.security.login_attempt import LoginAttempt, AuthenticationFailureReason, AttemptType
from app.core.exceptions import AuthenticationError, InvalidTokenError, AccountLockedError
from app.core.config import settings
from jose.exceptions import JWTError


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.customer_repo = CustomerRepository(db)
        self.session_repo = CustomerSessionRepository(db)
        self.login_attempt_repo = LoginAttemptRepository(db)

    async def register(self, email: str, password: str, first_name: str, last_name: Optional[str] = None) -> Customer:
        existing = await self.customer_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        hashed = hash_password(password)
        customer = Customer(
            email=email,
            password_hash=hashed,
            first_name=first_name,
            last_name=last_name,
            account_status=AccountStatus.ACTIVE,
            auth_provider=AuthProvider.EMAIL,
            is_admin=False,  # default
        )
        await self.customer_repo.create(customer)
        await self.db.commit()
        return customer

    async def authenticate(self, email: str, password: str, ip: str, user_agent: str) -> Optional[Customer]:
        customer = await self.customer_repo.get_by_email(email)
        if not customer:
            return None
        if customer.auth_provider != AuthProvider.EMAIL:
            return None
        if customer.account_status != AccountStatus.ACTIVE:
            return None
        if customer.locked_until and customer.locked_until > datetime.now(timezone.utc):
            raise AccountLockedError("Account temporarily locked")
        if not verify_password(password, customer.password_hash):
            await self._record_failed_attempt(customer, ip, user_agent)
            return None
        customer.failed_login_count = 0
        customer.last_login_at = datetime.now(timezone.utc)
        await self.customer_repo.save(customer)
        return customer

    async def _record_failed_attempt(self, customer: Customer, ip: str, user_agent: str):
        attempt = LoginAttempt(
            customer_id=customer.id,
            email=customer.email,
            ip_address=ip,
            user_agent=user_agent,
            successful=False,
            failure_reason=AuthenticationFailureReason.INVALID_CREDENTIALS,
            attempt_type=AttemptType.LOGIN,
        )
        await self.login_attempt_repo.create(attempt)
        customer.failed_login_count += 1
        if customer.failed_login_count >= settings.MAX_LOGIN_ATTEMPTS:
            customer.locked_until = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCOUNT_LOCK_MINUTES)
        await self.customer_repo.save(customer)

    async def create_session(self, customer: Customer, ip: str, user_agent: str):
        session = CustomerSession(
            customer_id=customer.id,
            refresh_token_hash="",  # placeholder
            ip_address=ip,
            user_agent=user_agent,
            login_at=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        await self.session_repo.create(session)
        # Generate refresh token with session public_id as subject
        refresh_token = create_refresh_token(str(session.public_id))
        session.refresh_token_hash = hash_refresh_token(refresh_token)
        await self.session_repo.save(session)
        await self.db.commit()
        # Access token with email as subject
        access_token = create_access_token(customer.email)
        return session, access_token, refresh_token

    async def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = verify_refresh_token(refresh_token)
        except JWTError:
            raise InvalidTokenError("Invalid refresh token")
        session_public_id = payload.get("sub")
        if not session_public_id:
            raise InvalidTokenError("Invalid refresh token payload")
        session = await self.session_repo.get_by_public_id(session_public_id)
        if not session or session.revoked_at is not None:
            raise InvalidTokenError("Session revoked or not found")
        if session.expires_at < datetime.now(timezone.utc):
            raise InvalidTokenError("Refresh token expired")
        if not verify_refresh_token_hash(refresh_token, session.refresh_token_hash):
            raise InvalidTokenError("Token mismatch")
        customer = await self.customer_repo.get_by_id(session.customer_id)
        if not customer:
            raise InvalidTokenError("Customer not found")
        return create_access_token(customer.email)

    async def revoke_session(self, refresh_token: str) -> None:
        try:
            payload = verify_refresh_token(refresh_token)
        except JWTError:
            raise InvalidTokenError("Invalid refresh token")
        session_public_id = payload.get("sub")
        if not session_public_id:
            raise InvalidTokenError("Invalid refresh token payload")
        session = await self.session_repo.get_by_public_id(session_public_id)
        if session:
            session.revoked_at = datetime.now(timezone.utc)
            session.last_activity = datetime.now(timezone.utc)
            await self.session_repo.save(session)
            await self.db.commit()

    async def change_password(self, customer: Customer, current_password: str, new_password: str) -> None:
        if customer.auth_provider != AuthProvider.EMAIL:
            raise ValueError("Cannot change password for Google-authenticated account")
        if not verify_password(current_password, customer.password_hash):
            raise ValueError("Current password incorrect")
        customer.password_hash = hash_password(new_password)
        await self.customer_repo.save(customer)