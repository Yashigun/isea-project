import unittest
from types import SimpleNamespace

from app.schemas.security import (
    AuditLogResponse,
    BlockedIPResponse,
    LoginAttemptResponse,
    RequestLogResponse,
    SecurityEventResponse,
)


class SecuritySchemaTests(unittest.TestCase):
    def test_security_response_schemas_accept_missing_timestamps(self):
        request_log = SimpleNamespace(
            public_id="req_1",
            method="GET",
            protocol="HTTP/1.1",
            source="web",
            outcome="success",
            route="/admin/security/requests",
            path="/admin/security/requests",
            query_string=None,
            status_code=200,
            response_time_ms=12,
            ip_address="127.0.0.1",
            user_agent="test-agent",
            country=None,
            city=None,
            created_at=None,
            customer_id=None,
        )

        login_attempt = SimpleNamespace(
            public_id="login_1",
            email="user@example.com",
            ip_address="127.0.0.1",
            user_agent="test-agent",
            successful=True,
            failure_reason=None,
            attempt_type="login",
            created_at=None,
            customer_id=None,
        )

        audit_log = SimpleNamespace(
            public_id="audit_1",
            action="login",
            entity_type="customer",
            entity_name="demo",
            entity_public_id="cust_1",
            old_data=None,
            new_data=None,
            ip_address="127.0.0.1",
            user_agent="test-agent",
            created_at=None,
            customer_id=None,
        )

        blocked_ip = SimpleNamespace(
            public_id="block_1",
            ip_address="127.0.0.1",
            reason="brute_force",
            blocked_by="admin",
            block_note=None,
            blocked_until=None,
            permanently_blocked=False,
            is_active=True,
            created_at=None,
        )

        security_event = SimpleNamespace(
            public_id="event_1",
            event_type="suspicious_login",
            severity="high",
            title="Login",
            description="Login attempt",
            ip_address="127.0.0.1",
            country=None,
            city=None,
            resolved=False,
            created_at=None,
            evidence=None,
        )

        self.assertIsNone(RequestLogResponse.model_validate(request_log).created_at)
        self.assertIsNone(LoginAttemptResponse.model_validate(login_attempt).created_at)
        self.assertIsNone(AuditLogResponse.model_validate(audit_log).created_at)
        self.assertIsNone(BlockedIPResponse.model_validate(blocked_ip).created_at)
        self.assertIsNone(SecurityEventResponse.model_validate(security_event).created_at)


if __name__ == "__main__":
    unittest.main()
