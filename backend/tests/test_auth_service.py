import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.services.security.auth_service import AuthService


class AuthServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_create_session_commits_after_persisting_refresh_token(self):
        db = AsyncMock()
        db.commit = AsyncMock()
        db.flush = AsyncMock()
        db.add = AsyncMock()

        service = AuthService(db)
        service.session_repo.create = AsyncMock(side_effect=lambda session: session)
        service.session_repo.save = AsyncMock(side_effect=lambda session: session)

        customer = SimpleNamespace(
            id="customer-id",
            email="user@example.com",
        )

        session, access_token, refresh_token = await service.create_session(
            customer,
            ip="127.0.0.1",
            user_agent="test-agent",
        )

        self.assertTrue(session.refresh_token_hash)
        self.assertTrue(access_token)
        self.assertTrue(refresh_token)
        db.commit.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
