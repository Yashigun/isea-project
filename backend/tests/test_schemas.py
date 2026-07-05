import unittest
from types import SimpleNamespace

from app.schemas.customer import CustomerPhoneResponseSchema


class SchemaTests(unittest.TestCase):
    def test_phone_response_schema_accepts_missing_timestamps(self):
        payload = SimpleNamespace(
            public_id="ph_123",
            phone_number="1234567890",
            is_default=True,
            created_at=None,
            updated_at=None,
        )

        result = CustomerPhoneResponseSchema.model_validate(payload)

        self.assertEqual(result.phone_number, "1234567890")
        self.assertTrue(result.is_default)
        self.assertIsNone(result.created_at)
        self.assertIsNone(result.updated_at)


if __name__ == "__main__":
    unittest.main()
