import hashlib
import secrets
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import AdminSession

SESSION_COOKIE_NAME = "admin_session"
SESSION_TTL_HOURS = 8


def hash_token(token: str) -> str:
    """Simpan token sebagai hash, biar bocor pun nggak bisa dipakai."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_admin_password(password: str) -> bool:
    if not settings.admin_password_hash:
        return False
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            settings.admin_password_hash.encode("utf-8"),
        )
    except ValueError:
        return False


def create_session(db: Session) -> str:
    """Bikin token acak, simpan hash-nya di DB, return token mentah utk cookie."""
    token = secrets.token_urlsafe(48)
    db.add(
        AdminSession(
            token_hash=hash_token(token),
            expires_at=datetime.utcnow() + timedelta(hours=SESSION_TTL_HOURS),
        )
    )
    db.commit()
    return token


def get_current_admin(request: Request, db: Session = Depends(get_db)) -> AdminSession:
    """Cek cookie sesi. Kalau nggak valid -> 401."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Belum login")

    row = (
        db.query(AdminSession)
        .filter(AdminSession.token_hash == hash_token(token))
        .filter(AdminSession.expires_at > datetime.utcnow())
        .first()
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesi habis")

    return row


def destroy_session(token: str, db: Session) -> None:
    db.query(AdminSession).filter(AdminSession.token_hash == hash_token(token)).delete()
    db.commit()