import hmac
from datetime import datetime
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth import (
    SESSION_COOKIE_NAME,
    create_session,
    destroy_session,
    get_current_admin,
    verify_admin_password,
)
from ..config import settings
from ..database import get_db
from ..models import AdminSession, PendingQuestion
from ..ratelimit import LoginRateLimiter

router = APIRouter()

login_limiter = LoginRateLimiter(
    max_failures=settings.login_max_failures,
    window_seconds=settings.login_window_seconds,
    lockout_seconds=settings.login_lockout_seconds,
)


class LoginIn(BaseModel):
    username: str
    password: str


class AnswerIn(BaseModel):
    answer: str


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@router.post("/api/admin/login")
def admin_login(
    payload: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)
):
    ip = _client_ip(request)
    wait = login_limiter.retry_after(ip)
    if wait is not None:
        raise HTTPException(
            status_code=429,
            detail=f"Terlalu banyak percobaan login. Coba lagi dalam {wait} detik.",
            headers={"Retry-After": str(wait)},
        )

    # Jalanin dua-duanya biar waktu respons sama, nggak kebaca mana yang salah.
    username_ok = hmac.compare_digest(payload.username.encode(), settings.admin_username.encode())
    password_ok = verify_admin_password(payload.password)
    if not (username_ok and password_ok):
        login_limiter.record_failure(ip)
        raise HTTPException(status_code=401, detail="Username atau password salah")

    login_limiter.reset(ip)
    token = create_session(db)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=8 * 60 * 60,
        path="/",
    )
    return {"ok": True}


@router.post("/api/admin/logout")
def admin_logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        destroy_session(token, db)
    response.delete_cookie(SESSION_COOKIE_NAME, path="/", secure=settings.cookie_secure)
    return {"ok": True}


@router.get("/api/admin/me")
def admin_me(session: AdminSession = Depends(get_current_admin)):
    return {"ok": True, "username": settings.admin_username}


@router.get("/api/admin/pending")
def list_pending(
    session: AdminSession = Depends(get_current_admin), db: Session = Depends(get_db)
):
    rows = db.query(PendingQuestion).order_by(PendingQuestion.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "question": r.question,
            "user_email": r.user_email,
            "status": r.status,
            "category": r.category,
            "answer": r.answer,
            "answered_at": r.answered_at.isoformat() if r.answered_at else None,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.post("/api/admin/pending/{question_id}/answer")
def answer_question(
    question_id: int,
    payload: AnswerIn,
    session: AdminSession = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    row = db.query(PendingQuestion).filter(PendingQuestion.id == question_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Pertanyaan tidak ditemukan")

    row.answer = payload.answer
    row.status = "answered"
    row.answered_at = datetime.utcnow()
    db.commit()
    return {"ok": True}


@router.post("/api/admin/pending/{question_id}/delete")
def delete_question(
    question_id: int,
    session: AdminSession = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    row = db.query(PendingQuestion).filter(PendingQuestion.id == question_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Pertanyaan tidak ditemukan")

    db.delete(row)
    db.commit()
    return {"ok": True}