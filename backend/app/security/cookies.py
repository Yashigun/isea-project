from __future__ import annotations

from datetime import timedelta

from fastapi import Response

from app.core.config import settings


ACCESS_COOKIE_NAME = "access_token"

REFRESH_COOKIE_NAME = "refresh_token"


def set_access_cookie(
    response: Response,
    access_token: str,
) -> None:
    """
    Store the access token in a secure
    HttpOnly cookie.
    """

    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        max_age=int(
            timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            ).total_seconds()
        ),
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
    )


def set_refresh_cookie(
    response: Response,
    refresh_token: str,
) -> None:
    """
    Store the refresh token in a secure
    HttpOnly cookie.
    """

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=int(
            timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            ).total_seconds()
        ),
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
    )


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
) -> None:
    """
    Store both authentication cookies.
    """

    set_access_cookie(
        response=response,
        access_token=access_token,
    )

    set_refresh_cookie(
        response=response,
        refresh_token=refresh_token,
    )


def clear_access_cookie(
    response: Response,
) -> None:
    """
    Remove the access token cookie.
    """

    response.delete_cookie(
        key=ACCESS_COOKIE_NAME,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
    )


def clear_refresh_cookie(
    response: Response,
) -> None:
    """
    Remove the refresh token cookie.
    """

    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
    )


def clear_auth_cookies(
    response: Response,
) -> None:
    """
    Remove all authentication cookies.
    """

    clear_access_cookie(response)

    clear_refresh_cookie(response)