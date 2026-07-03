from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.security.auth_service import AuthService
from app.schemas.auth import (
    RegisterRequestSchema,
    LoginRequestSchema,
    RefreshTokenRequestSchema,
    LogoutRequestSchema,
    ChangePasswordRequestSchema,
    AuthenticatedCustomerSchema,
    TokenResponseSchema,
)
from app.core.dependencies import get_current_user, get_client_ip, get_user_agent
from app.models.store.customer import Customer
from app.core.exceptions import AccountLockedError, InvalidTokenError
from app.security.cookies import (
    set_auth_cookies,
    clear_auth_cookies,
    ACCESS_COOKIE_NAME,
    REFRESH_COOKIE_NAME,
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthenticatedCustomerSchema)
async def register(
    payload: RegisterRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        customer = await service.register(
            email=payload.email,
            password=payload.password.get_secret_value(),
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return AuthenticatedCustomerSchema(
        public_id=customer.public_id,
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
    )


@router.post("/login")
async def login(
    payload: LoginRequestSchema,
    response: Response,
    db: AsyncSession = Depends(get_db),
    ip: str = Depends(get_client_ip),
    user_agent: str = Depends(get_user_agent),
):
    service = AuthService(db)
    try:
        customer = await service.authenticate(
            email=payload.email,
            password=payload.password.get_secret_value(),
            ip=ip,
            user_agent=user_agent,
        )
        if not customer:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except AccountLockedError as e:
        raise HTTPException(status_code=403, detail=str(e))

    session, access_token, refresh_token = await service.create_session(customer, ip, user_agent)
    set_auth_cookies(response, access_token, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "customer": {
            "public_id": customer.public_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
        },
    }


@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    # Try to get refresh token from cookie first
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        # fallback to request body (for mobile clients)
        body = await request.json()
        refresh_token = body.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token missing")

    service = AuthService(db)
    try:
        new_access = await service.refresh_access_token(refresh_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))

    # Update access cookie
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=new_access,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
    )

    return {
        "access_token": new_access,
        "token_type": "Bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if refresh_token:
        service = AuthService(db)
        try:
            await service.revoke_session(refresh_token)
        except InvalidTokenError:
            pass  # still clear cookies

    clear_auth_cookies(response)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=AuthenticatedCustomerSchema)
async def get_me(
    current_user: Customer = Depends(get_current_user),
):
    return AuthenticatedCustomerSchema(
        public_id=current_user.public_id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
    )


@router.post("/change-password")
async def change_password(
    payload: ChangePasswordRequestSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        await service.change_password(
            current_user,
            payload.current_password.get_secret_value(),
            payload.new_password.get_secret_value(),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Password changed successfully"}