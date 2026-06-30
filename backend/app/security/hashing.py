from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using Argon2id.
    """
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against its stored hash.
    """
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )


def needs_rehash(hashed_password: str) -> bool:
    """
    Check whether an existing password hash should be
    upgraded to the current Argon2 parameters.
    """
    return password_hasher.check_needs_rehash(
        hashed_password,
    )