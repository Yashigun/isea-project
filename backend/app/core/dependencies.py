from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.security.jwt import verify_access_token
from app.repositories.store.customer_repository import CustomerRepository
from app.models.store.customer import Customer, AccountStatus
from app.security.cookies import ACCESS_COOKIE_NAME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_token_from_request(request: Request) -> str:
    """
    Extract the JWT token from either the Authorization header
    or the secure HttpOnly cookie.
    """
    # 1. Try Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]

    # 2. Try cookie
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if token:
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    token: str = Depends(get_token_from_request),
    db: AsyncSession = Depends(get_db),
) -> Customer:
    """
    Retrieve the currently authenticated customer.
    """
    try:
        payload = verify_access_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    repo = CustomerRepository(db)
    customer = await repo.get_by_email(email)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if customer.account_status != AccountStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active",
        )

    # Store customer ID in request state for logging
    # (optional – used by request logging middleware)
    # request.state.customer_id = customer.id

    return customer


async def get_current_admin(
    current_user: Customer = Depends(get_current_user),
) -> Customer:
    """
    Ensure the current user has admin privileges.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from the request.
    """
    # Check for proxy-forwarded IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "0.0.0.0"


def get_user_agent(request: Request) -> str:
    """
    Extract User-Agent header from the request.
    """
    return request.headers.get("user-agent", "")