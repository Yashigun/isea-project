import unittest
from json import JSONDecodeError
from types import SimpleNamespace
from unittest.mock import AsyncMock

from fastapi import HTTPException, Response

from app.api.auth import refresh


class AuthApiTests(unittest.IsolatedAsyncioTestCase):
    async def test_refresh_returns_400_when_body_is_missing(self):
        request = SimpleNamespace(
            cookies={},
            json=AsyncMock(side_effect=JSONDecodeError("Expecting value", "", 0)),
        )

        with self.assertRaises(HTTPException) as context:
            await refresh(request, Response(), db=AsyncMock())

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Refresh token missing")


if __name__ == "__main__":
    unittest.main()
